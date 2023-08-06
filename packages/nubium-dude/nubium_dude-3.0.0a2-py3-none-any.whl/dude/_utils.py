# pylint: disable=no-self-argument,no-self-use,too-few-public-methods

import asyncio
from functools import wraps, partial
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

import click
from dotenv import dotenv_values, load_dotenv
import jsonpath_ng
from nubium_utils import _local_env_defaults as nubium_utils_vars
from pydantic import BaseSettings, Field, root_validator
import yaml


__all__ = [
    "DudeConfig",
    "DudeEnvironment",
    "KafkaCluster",
    "KafkaTopic",
    "TopicConfig",
]


class _OurBaseModel(BaseSettings):
    def __getitem__(self, item):
        return getattr(self, item)


def _yaml_safe_loader(cls):
    yaml.SafeLoader.add_constructor(cls.yaml_tag, cls.from_yaml)
    return cls


@_yaml_safe_loader
class DotEnvTag(yaml.YAMLObject):
    yaml_tag = "!DotEnv"

    @classmethod
    def from_yaml(cls, loader, node):
        path, var = node.value
        return dotenv_values(path.value)[var.value]


@_yaml_safe_loader
class EnvironmentTag(yaml.YAMLObject):
    yaml_tag = "!Environment"

    @classmethod
    def from_yaml(cls, loader, node):
        return os.environ[node.value]


@_yaml_safe_loader
class IncludeTag(yaml.YAMLObject):
    yaml_tag = "!Include"

    @classmethod
    def from_yaml(cls, loader, node):
        filename = loader.construct_scalar(node)
        with open(filename) as file:
            file_yaml = yaml.safe_load(file)
            return file_yaml


@_yaml_safe_loader
class JsonPathTag(yaml.YAMLObject):
    """
    More docs available at https://pypi.org/project/jsonpath-ng/
    """

    yaml_tag = "!JsonPath"

    @classmethod
    def from_yaml(cls, loader, node):
        query, corpus = loader.construct_sequence(node, deep=True)
        needle = jsonpath_ng.parse(query)
        haystack = yaml.safe_load(json.dumps(corpus))
        return needle.find(haystack)[0].value


@_yaml_safe_loader
class ParseYamlTag(yaml.YAMLObject):
    """
    When other tags give back a string, but parsed yaml is desired instead, this tag can help.
    """

    yaml_tag = "!ParseYaml"

    @classmethod
    def from_yaml(cls, loader, node):
        string_blob = loader.construct_sequence(node, deep=True)[0]
        return yaml.safe_load(string_blob)


@_yaml_safe_loader
class MergeTag(yaml.YAMLObject):
    yaml_tag = "!Merge"

    @classmethod
    def from_yaml(cls, loader, node):
        values = loader.construct_sequence(node, deep=True)
        result = {}
        for v in values:
            result.update(v)
        return result


class KafkaCluster(_OurBaseModel):
    bootstrap_urls: List[str]
    username: str = Field(default_factory=lambda: os.environ["RHOSAK_USERNAME"])
    password: str = Field(default_factory=lambda: os.environ["RHOSAK_PASSWORD"])

    def toolbox_dict(self):
        return {
            "url": ",".join(self.bootstrap_urls),
            "username": self.username,
            "password": self.password,
        }


class TopicConfig(_OurBaseModel):
    config: Dict[str, Any] = Field(default_factory=dict)
    partitions: int
    replication_factor: int


class KafkaTopic(_OurBaseModel):
    cluster: str
    configs: TopicConfig

    def toolbox_dict(self):
        return self.dict()


class DudeEnvironment(_OurBaseModel):
    clusters: Dict[str, KafkaCluster] = Field(default_factory=dict)
    dotenv_files: List[str] = Field(default_factory=list)
    target_namespace: Optional[str] = None
    topics: Dict[str, KafkaTopic] = Field(default_factory=dict)


class DudeConfig(_OurBaseModel):
    """
    The default location for this YAML configuration is based on whatever `click.get_app_dir("dude") / "config.yaml" <https://click.palletsprojects.com/en/8.0.x/api/#click.get_app_dir>`_ returns. You may override this location with the environment variable `DUDE_CONFIG_FILE`.
    """

    app_venv: str = Field(
        "./venv",
        env="DUDE_APP_VENV",
        description="A path relative to an app folder where dude will store an app's virtualenv.",
    )
    default_environment: Optional[str] = Field(
        None,
        description="Automatically select an environment to save on typing `dude --env_name ...`",
    )
    environments: Dict[str, DudeEnvironment] = Field(
        default_factory=dict,
        description="Main part of the configuration that is used for dev, staging, prod, and any other environments that need to be defined.",
    )
    refresh_secrets: Literal["always", "daily", "never", "weekly"] = Field(
        "never",
        description="Not implemented yet. TODO: after secrets are pulled from openshift, this setting should refresh secrets that are older than the configured setting.",
    )

    @root_validator(skip_on_failure=True)
    def must_be_an_environment_that_is_defined(cls, values):
        if values["default_environment"] and values["default_environment"] not in values["environments"]:
            raise ValueError("default_environment was not found in environments")
        return values


class ConfigManager:
    @staticmethod
    def get_config_path():
        if "DUDE_CONFIG_FILE" in os.environ:
            return Path(os.environ["DUDE_CONFIG_FILE"])
        app_dir = Path(click.get_app_dir("dude"))
        os.makedirs(app_dir, exist_ok=True)
        config_file = app_dir / "config.yaml"
        config_file.touch()  # TODO: generate example config
        return config_file

    def __init__(self):
        config_file = ConfigManager.get_config_path()
        yaml_dict = yaml.safe_load(open(config_file))
        if not isinstance(yaml_dict, dict):
            yaml_dict = {}
        self.config = DudeConfig.parse_obj(yaml_dict)

    def activate_environment(self, selected_environment):
        for dotenv in self.config.environments[selected_environment].dotenv_files:
            load_dotenv(dotenv, override=True)

    def get_cluster_dict(self, selected_environment):
        clusters = self.config.environments[selected_environment]["clusters"]
        return {c: clusters[c].toolbox_dict() for c in clusters}

    def get_topic_dict(self, selected_environment):
        topics = self.config.environments[selected_environment]["topics"]
        return {t: topics[t].toolbox_dict() for t in topics}

    def __str__(self):
        return yaml.safe_dump(self.config.dict())

    def __getitem__(self, item):
        return getattr(self.config, item)


def import_dotenvs():
    load_dotenv(f"{Path(nubium_utils_vars.__file__).parent}/local.env", override=True)


def as_async(func):
    """
    Turn any method into an async method by making a new, decorated method with this.
    """

    @wraps(func)
    async def run_as_async(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)

    return run_as_async

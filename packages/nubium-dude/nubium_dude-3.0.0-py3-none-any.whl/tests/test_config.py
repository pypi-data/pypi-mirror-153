import os
from unittest.mock import call, patch

from click.testing import CliRunner
import pydantic
import pytest
import yaml

from dude._commands.cli_base import dude_cli
from dude._utils import ConfigManager, DudeConfig
from .conftest import mock_config_file


def dotenv_config_gen(path: str) -> str:
    return f"""
environments:
  local:
    dotenv_files: [{path}]
"""


topics_defined_config = """
environments:
  local:
    clusters:
      A:
        bootstrap_urls: ["localhost", "kafka-1"]
    topics:
      Fun:
        cluster: A
        configs:
          config:
            cleanup.policy: delete
            retention.ms: 259200000
          partitions: 1
          replication_factor: 3
      House:
        cluster: A
        configs:
          config:
            cleanup.policy: delete
            retention.ms: 259200000
          partitions: 3
          replication_factor: 3
default_environment: local
"""


default_environment_config = """
environments:
  default:
    clusters:
      default-A:
        bootstrap_urls: ["localhost", "kafka-1"]
  override:
    clusters:
      override-A:
        bootstrap_urls: ["localhost", "kafka-1"]
default_environment: default
"""


environment_var_config = """
environments:
  breakfast:
    clusters:
      eggs:
        bootstrap_urls: ["i.hop"]
        username: !Environment USERNAME_SYRUP
    target_namespace: cracker--barrel
"""


fancy_config = """
environments:
  fancy:
    clusters:
      fancy-cluster:
        bootstrap_urls: ["somewhere.fancy"]
    target_namespace: tenant--default
"""


invalid_config = """
blah:
  invalid: something
"""


multi_config = """
environments:
  A:
    clusters:
      A:
        bootstrap_urls: ["localhost", "kafka-1"]
  B:
    clusters:
      B:
        bootstrap_urls: ["localhost", "kafka-1"]
"""


class TestCustomYamlTags:
    def test_they_work(self):
        expected = "TIME"
        with patch.dict(os.environ, {"PARTY": "TIME"}):
            actual = yaml.safe_load("!Environment PARTY")
            assert actual == expected

    def test_dotenv_loads_from_file(self, tmp_path):
        temp_file = tmp_path / "dot.env"
        temp_file.write_text("RED=THING 1\nHAT=THING 2")
        expected = {
            "BEST": "THING 1",
            "RHYMER": "THING 2",
        }
        actual = yaml.safe_load(
            f"""BEST: !DotEnv ["{temp_file}", RED]
RHYMER: !DotEnv ["{temp_file}", HAT]"""
        )
        assert actual == expected

    def test_including_yaml_from_file(self, tmp_path):
        temp_file = tmp_path / "inclusive.yaml"
        temp_file.write_text("recursion: !Environment RECURSION")
        expected = {"recursion": {"recursion": "RECURSION"}}
        with patch.dict(os.environ, {"RECURSION": "RECURSION"}):
            actual = yaml.safe_load(f"recursion: !Include {temp_file}")
        assert actual == expected

    def test_merge_can_work_with_include(self, tmp_path):
        temp_file = tmp_path / "extensible.yaml"
        temp_file.write_text("a: 1\nb: 2")
        expected = {"other": {"a": 1, "b": "override", "c": 3}}
        actual = yaml.safe_load(
            f"""
other: !Merge
  - !Include "{temp_file}"
  - b: override
    c: 3
        """
        )
        assert actual == expected

    def test_jsonpath_can_extract_portions_of_nested_yamls(self, tmp_path):
        temp_file = tmp_path / "inclusive.yaml"
        temp_file.write_text("bird: {nested: egg}\ntext-blob: |\n  yaml: true")
        expected = {"file-nesting": ["egg", {"yaml": True}], "inline": 42}
        actual = yaml.safe_load(
            f"""
file-nesting:
  - !JsonPath ["$.bird.nested", !Include "{temp_file}"]
  - !ParseYaml [!JsonPath ["$.text-blob", !Include "{temp_file}"]]
inline: !JsonPath [$.here, {{here: 42}}]
"""
        )
        assert actual == expected


def test_parsing_invalid_config_raises_validation_errors():
    yaml_dict = {
        "default_environment": "dev",
        "environments": {
            "dev": {
                "clusters": {
                    "nubium_0": {
                        "bootstrap_urls": ["dev-nubium-c--ungiev--a-i-khlog.bf2.kafka.rhcloud.com:443"],
                        "password": "redact",
                        "username": "redact",
                    }
                },
                "target_namespace": "mktg-ops--nubium-dev",
                "topics": [
                    {
                        "NubiumIntegrations_RedHatTV_ContactsRedHatTVRetriever_Timestamps": {
                            "cluster": 0,
                            "configs": {
                                "cleanup.policy": "compact",
                                "config": None,
                                "partitions": 1,
                                "replication_factor": 3,
                            },
                        }
                    }
                ],
            },
            "local": {
                "clusters": None,
                "lalala": {"bootstrap_urls": ["localhost"]},
                "target_namespace": "as-if-this-matters",
            },
        },
        "refresh_secrets": "daily",
    }
    with pytest.raises(pydantic.ValidationError) as exc:
        DudeConfig.parse_obj(yaml_dict)
    assert "value is not a valid dict" in str(exc.value)
    assert "none is not an allowed value" in str(exc.value)
    assert "extra fields not permitted" in str(exc.value)


class TestConfigManager:
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, mock_config_file):
        self.config_file = mock_config_file

    def test_default_environment_must_be_in_environments(self):
        self.config_file.write_text("environments: {here: {}}\ndefault_environment: not-here")
        with pytest.raises(pydantic.ValidationError):
            ConfigManager()

    def test_environment_can_override_default_config_file_location(self, tmp_path):
        self.config_file.write_text("Can't touch this")
        real_config_file = tmp_path / "mc.hammer"
        real_config_file.write_text(fancy_config)
        with patch.dict("os.environ", {"DUDE_CONFIG_FILE": str(real_config_file)}):
            config_manager = ConfigManager()
        assert config_manager["environments"]["fancy"]["target_namespace"] == "tenant--default"

    def test_exports_environment_variables_from_the_dotenv_section_when_environment_is_activated(self, tmp_path):
        temp_dotenv_file = tmp_path / "dot.env"
        temp_dotenv_file.write_text("LOOKATME=hands in the air like it's good to be\nFLO_RIDA=no handlebars")
        dotenv_config = dotenv_config_gen(temp_dotenv_file)
        self.config_file.write_text(dotenv_config)
        with patch.dict("os.environ", {"FLO_RIDA": "handlebars"}):
            config_manager = ConfigManager()
        assert "LOOKATME" not in os.environ

        config_manager.activate_environment("local")
        assert os.environ["LOOKATME"] == "hands in the air like it's good to be"
        assert os.environ["FLO_RIDA"] == "no handlebars"

    def test_has_sensible_defaults(self):
        config_manager = ConfigManager()
        assert config_manager["refresh_secrets"] == "never"

    def test_rejects_invalid_values(self):
        self.config_file.write_text("refresh_secrets: not_valid")
        with pytest.raises(pydantic.ValidationError):
            config_manager = ConfigManager()

    def test_supports_nested_cluster_options(self):
        self.config_file.write_text(fancy_config)
        config_manager = ConfigManager()
        assert config_manager["environments"]["fancy"]["target_namespace"] == "tenant--default"

    def test_cluster_names_that_are_missing_raise_an_exception(self):
        self.config_file.write_text(fancy_config)
        with patch.dict(os.environ, {"RHOSAK_USERNAME": "mock-username", "RHOSAK_PASSWORD": "mock-password"}):
            config_manager = ConfigManager()
            with pytest.raises(KeyError):
                config_manager.get_cluster_dict("fancy-typo")

    def test_translates_cluster_configuration_into_a_format_that_kakfa_toolbox_wants(self):
        self.config_file.write_text(fancy_config)
        expected = {
            "fancy-cluster": {
                "url": "somewhere.fancy",
                "username": "mock-username",
                "password": "mock-password",
            }
        }
        with patch.dict(os.environ, {"RHOSAK_USERNAME": "mock-username", "RHOSAK_PASSWORD": "mock-password"}):
            config_manager = ConfigManager()
            assert config_manager.get_cluster_dict("fancy") == expected

    def test_translates_topic_configuration_into_a_format_that_kakfa_toolbox_wants(self):
        self.config_file.write_text(topics_defined_config)
        expected = {
            "Fun": {
                "cluster": "A",
                "configs": {
                    "config": {
                        "cleanup.policy": "delete",
                        "retention.ms": 259200000,
                    },
                    "partitions": 1,
                    "replication_factor": 3,
                },
            },
            "House": {
                "cluster": "A",
                "configs": {
                    "config": {
                        "cleanup.policy": "delete",
                        "retention.ms": 259200000,
                    },
                    "partitions": 3,
                    "replication_factor": 3,
                },
            },
        }
        config_manager = ConfigManager()
        assert config_manager.get_topic_dict("local") == expected

    def test_supports_environment_variable_references(self):
        self.config_file.write_text(environment_var_config)
        with patch.dict(os.environ, {"USERNAME_SYRUP": "on pancakes"}):
            config_manager = ConfigManager()
            assert config_manager["environments"]["breakfast"]["clusters"]["eggs"]["username"] == "on pancakes"


class TestConfigCommand:
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, mock_config_file):
        self.config_file = mock_config_file
        self.runner = CliRunner()

    @patch("subprocess.call")
    def test_edit_launches_the_specified_executable(self, mock_sp_call):
        with patch.dict(os.environ, {"EDITOR": "echo"}):
            self.runner.invoke(dude_cli, ["config", "edit"])
        assert mock_sp_call.call_args == call(["echo", ConfigManager.get_config_path().as_posix()])
        with patch.dict(os.environ, {"VISUAL": "echo", "EDITOR": "not this one"}):
            self.runner.invoke(dude_cli, ["config", "edit"])
        assert mock_sp_call.call_args == call(["echo", ConfigManager.get_config_path().as_posix()])
        self.runner.invoke(dude_cli, ["config", "edit"])
        assert mock_sp_call.call_args == call(["vi", ConfigManager.get_config_path().as_posix()])

    @patch("subprocess.call")
    def test_edit_still_works_even_if_config_is_invalid(self, mock_sp_call):
        self.config_file.write_text(invalid_config)
        with patch.dict(os.environ, {"EDITOR": "echo"}):
            self.runner.invoke(dude_cli, ["config", "edit"])
        assert mock_sp_call.call_args == call(["echo", ConfigManager.get_config_path().as_posix()])

    def test_can_be_dumped(self):
        self.config_file.write_text("refresh_secrets: never")
        result = self.runner.invoke(dude_cli, ["config"])
        assert "environments: {}\n" in result.output
        assert "refresh_secrets: never\n" in result.output
        assert result.exit_code == 0

    def test_dumps_selected_configuration(self):
        self.config_file.write_text(fancy_config)
        result = self.runner.invoke(dude_cli, ["--environment=fancy", "config"])
        assert "environments:\n  fancy:\n" in result.output
        assert result.exit_code == 0

    def test_selecting_a_missing_environment_prints_error(self):
        self.config_file.write_text(fancy_config)
        result = self.runner.invoke(dude_cli, ["--not-present"])
        assert "No such option: --not-present\n" in result.output
        assert result.exit_code == 2

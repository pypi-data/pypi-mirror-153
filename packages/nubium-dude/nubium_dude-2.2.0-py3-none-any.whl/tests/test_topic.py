import json
import uuid

from click.testing import CliRunner
from dude._commands.cli_base import dude_cli, _options_from_config
import pytest

from .test_config import default_environment_config, multi_config


def test_prints_usage_when_no_arguments_are_provided():
    runner = CliRunner()
    result = runner.invoke(dude_cli, ["topics"])
    assert "Usage" in result.output
    assert result.exit_code == 0


def test_complains_about_lack_of_enviroment_selection():
    runner = CliRunner()
    result = runner.invoke(dude_cli, ["topics", "list"])
    assert "No environment was selected\n" in result.output
    assert result.exit_code != 0


def test_using_config_file_is_supported(mock_config_file):
    mock_config_file.write_text(multi_config)
    _options_from_config(dude_cli)
    runner = CliRunner()
    result = runner.invoke(dude_cli, ["--A", "topics", "list"])
    actual = json.loads(result.output)
    assert "A" in actual
    assert isinstance(actual["A"], list)
    assert result.exit_code == 0


def test_default_environment_allows_for_less_typing(mock_config_file):
    mock_config_file.write_text(default_environment_config)
    _options_from_config(dude_cli)
    runner = CliRunner()
    result = runner.invoke(dude_cli, ["topics", "list"])
    print(result.output)
    actual = json.loads(result.output)
    assert "default-A" in actual
    assert isinstance(actual["default-A"], list)
    assert result.exit_code == 0


def test_default_environment_can_be_manually_overriden(mock_config_file):
    mock_config_file.write_text(default_environment_config)
    _options_from_config(dude_cli)
    runner = CliRunner()
    result = runner.invoke(dude_cli, ["--override", "topics", "list"])
    print(result.output)
    actual = json.loads(result.output)
    assert "override-A" in actual
    assert isinstance(actual["override-A"], list)
    assert result.exit_code == 0


def test_topics_can_be_created_and_erased(mock_config_file):
    mock_config_file.write_text(multi_config)
    _options_from_config(dude_cli)
    runner = CliRunner()
    topic_name = f"TestTopicsCanBeCreatedAndErased-{uuid.uuid4()}"

    creation_result = runner.invoke(
        dude_cli, ["--A", "topics", "create", "--topics", topic_name, "--replication-factor=1"]
    )
    assert creation_result.exit_code == 0, creation_result.output
    creation_list = runner.invoke(dude_cli, ["--A", "topics", "list"])
    topics = json.loads(creation_list.output)
    assert topic_name in topics["A"]
    assert creation_list.exit_code == 0

    deletion_result = runner.invoke(dude_cli, ["--B", "topics", "delete", "--topics", topic_name])
    assert deletion_result.exit_code == 0, deletion_result.output
    deletion_list = runner.invoke(dude_cli, ["--B", "topics", "list"])
    topics = json.loads(deletion_list.output)
    assert topic_name not in topics["B"]
    assert creation_list.exit_code == 0

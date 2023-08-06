from unittest.mock import patch

from click.testing import CliRunner
import pytest

from dude.__main__ import dude_cli
from dude import __version__
from .utils import IsolatedFixtureFolder


@pytest.mark.parametrize("unfininshed_command", ["lint"])
def test_unfinished_commands_print_todo(unfininshed_command):
    runner = CliRunner()
    result = runner.invoke(dude_cli, [unfininshed_command])
    assert "TODO" in result.output
    assert result.exit_code == 0


def test_prints_usage_when_no_arguments_are_provided():
    runner = CliRunner()
    result = runner.invoke(dude_cli)
    assert "Usage" in result.output
    assert result.exit_code == 0


def test_format_works():
    runner = CliRunner()
    with IsolatedFixtureFolder(runner, "formatting"):
        result = runner.invoke(dude_cli, ["format"])
        assert "reformatted kappa.py\nAll done! ✨ 🍰 ✨" in result.output
        assert result.exit_code == 0


def test_help_option_prints_usage():
    runner = CliRunner()
    result = runner.invoke(dude_cli, ["--help"])
    assert "Usage" in result.output
    assert result.exit_code == 0


def test_prints_the_correct_version():
    runner = CliRunner()
    result = runner.invoke(dude_cli, ["--version"])
    assert f"dude, version {__version__}" in result.output
    assert result.exit_code == 0


def test_unexpected_exceptions_are_logged():
    runner = CliRunner()
    with patch("dude._commands.cli_base.print_help", side_effect=RuntimeError("💥 boom 💥")):
        result = runner.invoke(dude_cli)
        assert "boom" in result.output
        assert result.exit_code != 0

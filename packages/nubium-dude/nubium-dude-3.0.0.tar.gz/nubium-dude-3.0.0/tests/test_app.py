from click.testing import CliRunner
import pytest

from dude._commands.cli_base import dude_cli
from .test_config import default_environment_config
from .utils import IsolatedFixtureFolder


class TestVirtualEnvironmentManager:
    @pytest.fixture(autouse=True)
    def setup(self, mock_config_file):
        self.runner = CliRunner()
        self.config_file = mock_config_file
        self.config_file.write_text(default_environment_config)

    def test_creation_of_virtual_environment(self):
        with IsolatedFixtureFolder(self.runner, "requirements-only"):
            result = self.runner.invoke(dude_cli, ["app", "unit_test"])
            assert "no tests ran" in result.output

            # Running it again in an already synced environment
            result = self.runner.invoke(dude_cli, ["--environment=default", "app", "unit_test"])
            assert "Everything up-to-date" in result.output
            assert "no tests ran" in result.output

    def test_sync_works(self):
        with IsolatedFixtureFolder(self.runner, "requirements-only"):
            result = self.runner.invoke(dude_cli, ["app", "sync"])
            assert "Successfully installed" in result.output

            result = self.runner.invoke(dude_cli, ["app", "sync"])
            assert "Successfully installed" not in result.output

            result = self.runner.invoke(dude_cli, ["app", "sync", "--wipe-existing"])
            assert "Successfully installed" in result.output

import os
from pathlib import Path
import shutil

from click.testing import CliRunner
import pytest


class IsolatedFixtureFolder:
    def __init__(self, runner: CliRunner, fixture_name: str):
        self.runner = runner
        self.fixture_source_folder = Path(os.getcwd()) / "tests" / "fixtures" / fixture_name
        self.fixture_name = fixture_name

    def __enter__(self):
        self.filesystem = self.runner.isolated_filesystem()
        self.filesystem.__enter__()
        dest = Path(os.getcwd()) / self.fixture_name
        shutil.copytree(self.fixture_source_folder, dest)
        os.chdir(dest)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.filesystem.__exit__(exc_type, exc_val, exc_tb)

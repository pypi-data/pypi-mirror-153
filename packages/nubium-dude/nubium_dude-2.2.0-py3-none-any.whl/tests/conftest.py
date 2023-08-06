import os
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True, scope="session")
def clean_environment():
    patched_env = {
        "HOSTNAME": "lazy-host",
        "NU_APP_NAME": "If debugging is the process of removing bugs, then programming must be the process of putting them in. (Edsger Dijkstra)",
        "NU_SCHEMA_REGISTRY_URL": "N/A unit-testing",
        "RHOSAK_USERNAME": "ninja-user",
        "RHOSAK_PASSWORD": "top-secret",
    }
    if "LANG" in os.environ:
        patched_env["LANG"] = os.environ["LANG"]
    with patch.dict(os.environ, patched_env, clear=True):
        yield


@pytest.fixture(autouse=True, scope="function")
def mock_config_file(tmp_path, clean_environment):
    with patch("dude._utils.click.get_app_dir", return_value=str(tmp_path)):
        yield tmp_path / "config.yaml"

# test_config_manager.py
import pytest
import yaml
from pathlib import Path
from dspyfun import DspyfunConfig
from dspyfun.config_manager import ConfigManager
import dspyfun.utils.path_tools as path_tools


@pytest.fixture
def temp_config_file(tmp_path, monkeypatch):
    # Create a temporary config directory and file
    config_path = tmp_path / "dspyfun_config.yaml"
    config_data = {
        "cluster_name": "test-cluster",
        "zone": "us-central1",
        "project_id": "test-project"
    }
    with open(config_path, 'w') as file:
        yaml.dump(config_data, file)

    # Override the config_dir function to use the temporary path
    def mock_config_dir():
        return tmp_path

    monkeypatch.setattr(path_tools, 'config_dir', mock_config_dir)

    yield config_path


def test_load_config(temp_config_file, monkeypatch):
    # Ensure the config_dir is mocked for this test
    def mock_config_dir():
        return temp_config_file.parent

    monkeypatch.setattr(path_tools, 'config_dir', mock_config_dir)

    config_manager = ConfigManager()
    config = config_manager.config

    assert config.cluster_name == "test-cluster"
    assert config.zone == "us-central1"
    assert config.project_id == "test-project"


def test_update_config(temp_config_file, monkeypatch):
    # Ensure the config_dir is mocked for this test
    def mock_config_dir():
        return temp_config_file.parent

    monkeypatch.setattr(path_tools, 'config_dir', mock_config_dir)

    config_manager = ConfigManager()
    config_manager.update_config(cluster_name="new-cluster", zone="us-east1")
    config = config_manager.config

    assert config.cluster_name == "new-cluster"
    assert config.zone == "us-east1"
    assert config.project_id == "test-project"


def test_save_config(temp_config_file, monkeypatch):
    # Ensure the config_dir is mocked for this test
    def mock_config_dir():
        return temp_config_file.parent

    monkeypatch.setattr(path_tools, 'config_dir', mock_config_dir)

    config_manager = ConfigManager()
    config_manager.update_config(cluster_name="new-cluster", zone="us-east1")

    with open(temp_config_file, 'r') as file:
        config_data = yaml.safe_load(file)

    assert config_data["cluster_name"] == "new-cluster"
    assert config_data["zone"] == "us-east1"
    assert config_data["project_id"] == "test-project"


def test_sync_config(temp_config_file, monkeypatch):
    # Ensure the config_dir is mocked for this test
    def mock_config_dir():
        return temp_config_file.parent

    monkeypatch.setattr(path_tools, 'config_dir', mock_config_dir)

    config_manager = ConfigManager()
    config_manager.update_config(cluster_name="synced-cluster", project_id="synced-project")
    config = config_manager.config

    assert config.cluster_name == "synced-cluster"
    assert config.zone == "us-central1"  # Unchanged
    assert config.project_id == "synced-project"

    with open(temp_config_file, 'r') as file:
        config_data = yaml.safe_load(file)

    assert config_data["cluster_name"] == "synced-cluster"
    assert config_data["zone"] == "us-central1"  # Unchanged
    assert config_data["project_id"] == "synced-project"

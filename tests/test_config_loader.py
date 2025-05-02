import os
import pytest
import yaml
from pathlib import Path
from config_loader import load_config

@pytest.fixture
def temp_config_file(tmp_path):
    """Creates a temporary YAML config file ending in 'atdm_flow.yaml'."""
    config_path = tmp_path / "demo.atdm_flow.yaml"
    config_data = {
        "platform": "ios",
        "device_name": "iPhone 14"
    }
    with open(config_path, 'w') as f:
        yaml.dump(config_data, f)
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    yield config_path
    os.chdir(old_cwd)

def test_load_config_success(temp_config_file):
    """Test that load_config() correctly reads a valid matching YAML file."""
    config = load_config()
    assert config["platform"] == "ios"
    assert config["device_name"] == "iPhone 14"

def test_load_config_file_not_found(tmp_path):
    """Test that load_config() raises FileNotFoundError when no matching file exists."""
    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        load_config()
    os.chdir(old_cwd)

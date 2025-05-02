import pytest
from unittest.mock import patch
from emulator_launcher import EmulatorLauncher

def test_launch_android_emulator_headless():
    """Test launching an Android emulator in headless mode with correct arguments."""
    launcher = EmulatorLauncher()
    with patch('subprocess.run') as mock_run:
        launcher.launch(platform='android', device_name='Pixel_5_API_30', headless=True)
        mock_run.assert_called_with([
            'emulator', '-avd', 'Pixel_5_API_30', '-no-window', '-no-audio', '-no-boot-anim'
        ], check=True)

def test_launch_android_emulator_gui():
    """Test launching an Android emulator with GUI (non-headless)."""
    launcher = EmulatorLauncher()
    with patch('subprocess.run') as mock_run:
        launcher.launch(platform='android', device_name='Pixel_6_Pro', headless=False)
        mock_run.assert_called_with([
            'emulator', '-avd', 'Pixel_6_Pro'
        ], check=True)

def test_launch_ios_simulator():
    """Test launching an iOS simulator using simctl boot."""
    launcher = EmulatorLauncher()
    with patch('subprocess.run') as mock_run:
        launcher.launch(platform='ios', device_name='iPhone 14', headless=True)
        mock_run.assert_called_with([
            'xcrun', 'simctl', 'boot', 'iPhone 14'
        ], check=True)

def test_launch_invalid_platform():
    """Test that an unsupported platform raises a ValueError."""
    launcher = EmulatorLauncher()
    with pytest.raises(ValueError):
        launcher.launch(platform='windows_phone', device_name='Lumia_950')
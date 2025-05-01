import pytest
from unittest.mock import patch
from emulator_launcher import EmulatorLauncher

def test_launch_android_emulator_headless():
    launcher = EmulatorLauncher()
    with patch('subprocess.run') as mock_run:
        launcher.launch(platform='android', device_name='Pixel_5_API_30', headless=True)
        mock_run.assert_called_with([
            'emulator', '-avd', 'Pixel_5_API_30', '-no-window', '-no-audio', '-no-boot-anim'
        ], check=True)

def test_launch_android_emulator_gui():
    launcher = EmulatorLauncher()
    with patch('subprocess.run') as mock_run:
        launcher.launch(platform='android', device_name='Pixel_6_Pro', headless=False)
        mock_run.assert_called_with([
            'emulator', '-avd', 'Pixel_6_Pro'
        ], check=True)

def test_launch_ios_simulator():
    launcher = EmulatorLauncher()
    with patch('subprocess.run') as mock_run:
        launcher.launch(platform='ios', device_name='iPhone 14', headless=True)
        mock_run.assert_called_with([
            'xcrun', 'simctl', 'boot', 'iPhone 14'
        ], check=True)

def test_launch_invalid_platform():
    launcher = EmulatorLauncher()
    with pytest.raises(ValueError):
        launcher.launch(platform='windows_phone', device_name='Lumia_950')

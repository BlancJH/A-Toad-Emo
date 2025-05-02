import pytest
import os
from unittest.mock import patch
from app_installer import AppInstaller

def test_install_android_success():
    """Test successful Android APK installation."""
    installer = AppInstaller()
    with patch('os.path.exists', return_value=True), \
         patch('subprocess.run') as mock_run:
        installer.install('android', 'emulator-5554', './app-release.apk')
        mock_run.assert_called_with(['adb', 'install', '-r', './app-release.apk'], check=True)

def test_install_ios_success():
    """Test successful iOS .app installation to simulator."""
    installer = AppInstaller()
    with patch('os.path.exists', return_value=True), \
         patch('subprocess.run') as mock_run:
        installer.install('ios', 'iPhone 14', './Runner.app')
        mock_run.assert_called_with(['xcrun', 'simctl', 'install', 'iPhone 14', './Runner.app'], check=True)

def test_app_file_not_found():
    """Test FileNotFoundError is raised if app file path does not exist."""
    installer = AppInstaller()
    with patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            installer.install('android', 'emulator-5554', './not_found.apk')

def test_unsupported_platform():
    """Test ValueError is raised for unsupported platform."""
    installer = AppInstaller()
    with patch('os.path.exists', return_value=True):
        with pytest.raises(ValueError):
            installer.install('windows_phone', 'lumia', './app.exe')

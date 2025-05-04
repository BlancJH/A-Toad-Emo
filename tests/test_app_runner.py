import pytest
from unittest.mock import patch, mock_open
from app_runner import AppRunner

@pytest.fixture
def runner():
    return AppRunner()

def test_get_android_package_id_success(runner):
    mock_output = "package: name='com.example.app' versionCode='1' versionName='1.0'"
    with patch('subprocess.check_output', return_value=mock_output):
        package_id = runner.get_android_package_id('./dummy.apk')
        assert package_id == 'com.example.app'

def test_get_android_package_id_failure(runner):
    with patch('subprocess.check_output', side_effect=Exception("aapt error")):
        with pytest.raises(RuntimeError, match="Failed to extract Android package name"):
            runner.get_android_package_id('./dummy.apk')

def test_get_ios_bundle_id_success(runner):
    mock_plist = {'CFBundleIdentifier': 'com.example.ios'}
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data=b'binary')), \
         patch('plistlib.load', return_value=mock_plist):
        bundle_id = runner.get_ios_bundle_id('./Runner.app')
        assert bundle_id == 'com.example.ios'

def test_get_ios_bundle_id_missing_file(runner):
    with patch('os.path.exists', return_value=False):
        with pytest.raises(RuntimeError, match="Info.plist not found"):
            runner.get_ios_bundle_id('./Runner.app')

def test_get_ios_bundle_id_missing_key(runner):
    with patch('os.path.exists', return_value=True), \
         patch('builtins.open', mock_open(read_data=b'binary')), \
         patch('plistlib.load', return_value={}):
        with pytest.raises(RuntimeError, match="CFBundleIdentifier not found"):
            runner.get_ios_bundle_id('./Runner.app')

def test_run_android_app(runner):
    with patch.object(AppRunner, 'get_android_package_id', return_value='com.example.app'), \
         patch('subprocess.run') as mock_run:
        runner.run_app('android', './dummy.apk')
        mock_run.assert_called_with(['adb', 'shell', 'monkey', '-p', 'com.example.app', '-c', 'android.intent.category.LAUNCHER', '1'], check=True)

def test_run_ios_app(runner):
    with patch.object(AppRunner, 'get_ios_bundle_id', return_value='com.example.ios'), \
         patch('subprocess.run') as mock_run:
        runner.run_app('ios', './Runner.app')
        mock_run.assert_called_with(['xcrun', 'simctl', 'launch', 'booted', 'com.example.ios'], check=True)

def test_run_unsupported_platform(runner):
    with pytest.raises(ValueError, match="Unsupported platform"):
        runner.run_app('blackberry', './app.bar')

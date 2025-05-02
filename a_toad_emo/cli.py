from emulator_launcher import EmulatorLauncher
from config_loader import load_config

def main():
    config = load_config()
    platform = config.get("platform")
    device_name = config.get("device_name")

    if not platform or not device_name:
        raise ValueError("Config must include 'platform' and 'device_name'.")

    launcher = EmulatorLauncher()
    launcher.launch(platform=platform, device_name=device_name, headless=True)

if __name__ == "__main__":
    main()
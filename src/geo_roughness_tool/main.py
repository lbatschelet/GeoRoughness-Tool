import os
import sys
import requests
import time
from packaging import version
import importlib.metadata
from colorama import Fore, Style

# Ensure the package is in the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from geo_roughness_tool.cli_main import CLIMain
from geo_roughness_tool.gui_main import main as main_gui
from geo_roughness_tool.log_config import setup_logging


def check_for_updates():
    """
    Check for updates by querying the PyPI API for the latest version of the package.

    Returns:
        bool: True if an update is available, False otherwise.
        str: The latest version available.
    """
    package_name = "geo-roughness-tool"
    pypi_url = f"https://pypi.org/pypi/{package_name}/json"

    try:
        response = requests.get(pypi_url)
        response.raise_for_status()
        data = response.json()
        latest_version = data['info']['version']
        current_version = importlib.metadata.version(package_name)

        if version.parse(latest_version) > version.parse(current_version):
            print(f"\n\n{Fore.RED}{Style.BRIGHT}*** IMPORTANT UPDATE AVAILABLE ***")
            print(f"You are running version {current_version}.")
            print(f"Version {latest_version} is available.")
            print("Run 'pip install --upgrade geo-roughness-tool' to update to the latest version.")
            print(f"*******************************{Style.RESET_ALL}\n\n")
            time.sleep(5)  # Pause for 5 seconds to ensure the message is read
            return True, latest_version
    except requests.RequestException as e:
        print(f"Could not check for updates: {e}")
    except importlib.metadata.PackageNotFoundError:
        print(f"Package '{package_name}' not found.")

    return False, None


def main():
    setup_logging()
    update_available, latest_version = check_for_updates()
    if update_available:
        print(f"Please update the package to version {latest_version}.")

    if len(sys.argv) > 1:
        print("Running in CLI mode...")
        cli = CLIMain()
        cli.run()
    else:
        print("Running in GUI mode...")
        main_gui()


if __name__ == "__main__":
    main()

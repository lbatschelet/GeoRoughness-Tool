"""
main.py
-------
Version: 1.3.0
Author: Lukas Batschelet
Date: 14.05.2024
-------
This module is the main entry point for the application.
"""

import sys

from cli_main import CLIMain
from gui_main import main as main_gui
from log_config import setup_logging


def main():
    setup_logging()
    if len(sys.argv) > 1:
        print("Running in CLI mode...")
        cli = CLIMain()
        cli.run()
    else:
        print("Running in GUI mode...")
        main_gui()


if __name__ == "__main__":
    main()

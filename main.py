import sys

from roughness_calculator.cli_main import CLIMain
from roughness_calculator.log_config import setup_logging
from roughness_calculator.new_gui_main import main as MainGUI


def main():
    setup_logging()
    if len(sys.argv) > 1:
        print("Running in CLI mode...")
        cli = CLIMain()
        cli.run()
    else:
        print("Running in GUI mode...")
        MainGUI()


if __name__ == "__main__":
    main()

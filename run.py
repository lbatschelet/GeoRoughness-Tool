import sys
from roughness_calculator.gui_main import main as gui_main
from roughness_calculator.cli_main import CLIMain

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--cli':
            print("Running in CLI mode...")
            cli = CLIMain()
            cli.run()
        else:
            print("Unknown command. Running in GUI mode...")
            gui_main()
    else:
        print("Running in GUI mode...")
        gui_main()

if __name__ == "__main__":
    main()

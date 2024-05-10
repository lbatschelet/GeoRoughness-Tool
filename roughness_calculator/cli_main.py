"""
cli_main.py
-----------
Version: 1.2.1
Author: Lukas Batschelet
Date: 11.05.2024
-----------
"""
import argparse
import logging
import sys

from roughness_calculator.classes.application_driver import ApplicationDriver
from roughness_calculator.classes.processing_parameters import ProcessingParameters

logger = logging.getLogger(__name__)


class CLIMain:
    def __init__(self) -> None:
        """
        Initialize the command line interface for the application.
        """
        self.parser = argparse.ArgumentParser(
            description="Tool for processing GeoTIFF DEM files to calculate and categorize surface roughness. \n"
                        "Running the command without any arguments will start a Graphical User Interface."

        )
        self.setup_arguments()

    def setup_arguments(self) -> None:
        """
        Set up command line arguments for the application.
        """
        # Mandatory arguments
        self.parser.add_argument('input_path', type=str,
                                 help='The path to the input GeoTIFF file.')
        self.parser.add_argument('output_dir', type=str,
                                 help='The path to the output directory.')

        # Optional arguments with defaults managed in the ProcessingParameters class
        self.parser.add_argument('--window_size', type=float,
                                 help='The side length of the square window in meters.')
        self.parser.add_argument('--band_number', type=int,
                                 help='The band number to be processed.')
        self.parser.add_argument('--high_value_threshold', type=float,
                                 help='The threshold for high values to be filtered out.')
        self.parser.add_argument('--category_thresholds', type=str,
                                 help='Comma-separated thresholds to categorize data.')

    def run(self) -> None:
        """
        Execute the command line interface.
        """
        args = self.parser.parse_args()

        # Convert the args to a dictionary and create ProcessingParameters
        params_dict = {
            'input_path': args.input_path,
            'output_dir': args.output_dir,
            'window_size': args.window_size,
            'band_number': args.band_number,
            'high_value_threshold': args.high_value_threshold,
            'category_thresholds': args.category_thresholds
        }
        # Remove None values explicitly to handle optional parameters correctly
        filtered_params = {k: v for k, v in params_dict.items() if v is not None}

        try:
            # Create ProcessingParameters instance using the factory method
            processing_params = ProcessingParameters.create_from_dict(filtered_params)

            # Initialize and run the application driver with the validated and converted parameters
            driver = ApplicationDriver(processing_params)
            driver.run()

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    cli = CLIMain()
    cli.run()


def main() -> None:
    """
    Entry point for the CLI.

    This method initializes the CLIMain class and runs it.

    Returns:
        None
    """
    # Initialize the CLIMain class
    cli_main = CLIMain()

    # Run the CLIMain class
    cli_main.run()


if __name__ == '__main__':
    main()

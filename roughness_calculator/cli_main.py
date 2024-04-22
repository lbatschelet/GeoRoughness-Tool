"""
cli_main.py
-----------
Version: 1.0.6
Author: Lukas Batschelet
Date: 22.04.2024
-----------
"""
from roughness_calculator.classes.application_driver import ApplicationDriver
import logging
from .log_config import setup_logging
import argparse
from typing import NoReturn

# Ensure the logger is set up (optional if you know `log_config.py` is already imported elsewhere)
setup_logging()

logger = logging.getLogger(__name__)


class CLIMain:
    def __init__(self) -> NoReturn:
        """
        Initialize the command line interface for the application.

        This method sets up the argument parser for the command line interface.

        Returns:
            None
        """
        # Initialize the argument parser with a description
        self.parser = argparse.ArgumentParser(
            description="CLI tool for processing GeoTIFF files to calculate surface roughness."
        )
        # Set up the command line arguments
        self.setup_arguments()

    def setup_arguments(self) -> None:
        """
        Set up command line arguments.

        This method configures the command line arguments for the application.

        Returns:
            None
        """
        # Add argument for the input GeoTIFF file path
        self.parser.add_argument('input_path', type=str, help='The path to the input GeoTIFF file.')

        # Add argument for the output directory path
        self.parser.add_argument('output_dir', type=str, help='The path to the output directory.')

        # Add optional argument for the window size with a default value of 1.0
        self.parser.add_argument('--window_size', type=float, default=1.0,
                                 help='The side length of the square window in meters. Default is 1.')

        # Add optional argument for the band number to be processed with a default value of 1
        self.parser.add_argument('--band_number', type=int, default=1,
                                 help='The band number to be processed. Default is 1.')

        # Add optional argument for the high value threshold with a default value of 1.0
        self.parser.add_argument('--high_value_threshold', type=float, default=1.0,
                                 help='The threshold for high values to be filtered out. Default is 1.0.')

        # Add optional argument for the categorical thresholds
        self.parser.add_argument('--categorical_thresholds', type=float, nargs='+',
                                 help='List of thresholds to categorize data.')

    def run(self) -> None:
        """
        Execute the command line interface.

        This method parses the command line arguments and initializes the ApplicationDriver with these arguments.
        It then runs the ApplicationDriver.

        Returns:
            None
        """
        # Parse the command line arguments
        args = self.parser.parse_args()

        # Initialize the ApplicationDriver with the parsed arguments
        driver = ApplicationDriver(
            input_path=args.input_path,
            output_dir=args.output_dir,
            window_size=args.window_size,
            band_number=args.band_number,
            high_value_threshold=args.high_value_threshold,
            categorical_thresholds=args.categorical_thresholds
        )

        # Run the ApplicationDriver
        driver.run()


def main() -> None:
    """
    Entry point for the CLI.

    This method initializes the CLIMain class and runs it.

    Returns:
        None
    """
    # Initialize the CLIMain class
    cli = CLIMain()

    # Run the CLIMain class
    cli.run()


if __name__ == '__main__':
    main()

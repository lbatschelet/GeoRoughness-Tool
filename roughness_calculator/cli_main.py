"""
cli_main.py
-----------
Version: 1.0.4
Author: Lukas Batschelet
Date: 21.04.2024
-----------
"""
import argparse
from roughness_calculator.classes.application_driver import ApplicationDriver
import logging
from .log_config import setup_logging

# Ensure the logger is set up (optional if you know `log_config.py` is already imported elsewhere)
setup_logging()

logger = logging.getLogger(__name__)


class CLIMain:
    def __init__(self) -> None:
        """
        Initializes the command line interface for the application.

        This method sets up the argument parser for the command line interface.
        """
        self.parser = (argparse.ArgumentParser(
            description="CLI tool for processing GeoTIFF files to calculate surface roughness."))
        self.setup_arguments()

    def setup_arguments(self) -> None:
        """
        Defines the command line arguments for the application.

        This method adds the necessary arguments to the argument parser.
        """
        # Define command line arguments
        self.parser.add_argument('input_path', type=str,
                                 help='The path to the input GeoTIFF file.')
        self.parser.add_argument('output_dir', type=str,
                                 help='The path to the output directory.')
        self.parser.add_argument('--window_size', type=float, default=1.0,
                                 help='The side length of the square window in meters. Default is 1.')
        self.parser.add_argument('--band_number', type=int, default=1,
                                 help='The band number to be processed. Default is 1.')
        self.parser.add_argument('--high_value_threshold', type=float, default=1.0,
                                 help='The threshold for high values to be filtered out. Default is 1.0.')
        self.parser.add_argument('--categorical_thresholds', type=float, nargs='+',
                                 help='List of thresholds to categorize data.')

    def run(self) -> None:
        """
        Runs the application with the provided command line arguments.

        This method parses the command line arguments and creates an instance of the
        ApplicationDriver class with these arguments. It then runs the application driver.
        """
        args = self.parser.parse_args()

        # Create and run the application driver with provided arguments
        driver = ApplicationDriver(
            input_path=args.input_path,
            output_dir=args.output_dir,
            window_size=args.window_size,
            band_number=args.band_number,
            high_value_threshold=args.high_value_threshold,
            categorical_thresholds=args.categorical_thresholds
        )
        driver.run()


if __name__ == '__main__':
    cli = CLIMain()
    cli.run()

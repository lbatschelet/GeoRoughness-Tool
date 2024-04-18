"""
application_driver.py
---------------------
Version: 1.0.0
Author: Lukas Batschelet
Date: 18.04.2024
---------------------
This module contains the ApplicationDriver class which is responsible for running the application.
It acts as a sort of interface between the calling User Interface (UI) and the GeoTIFFProcessor class.
This enables the separation of concerns and allows for easier testing and maintenance of the code.
(i.e. the UI does not need to know how the processing is done, it just needs to know how to call the processing.)
"""

import logging
import os

from geo_tiff_processor import GeoTIFFProcessor


class ApplicationDriver:
    def __init__(self, input_path, output_dir, window_size=1, band_number=1, high_value_threshold=1):
        """
        Initializes the ApplicationDriver with the input and output paths.

        :param str input_path: The path to the input GeoTIFF file.
        :param str output_dir: The path to the output directory.
        :param int window_size: The side length of the square window in meters. Default is 1.
        :param int band_number: The band number to be processed. Default is 1.
        :param int high_value_threshold: The threshold for high values to be filtered out. Default is 1.
        :raises FileNotFoundError: If the input path or output directory is not valid.
        """
        self.setup_logging()
        self.input_path = input_path
        self.output_dir = output_dir

        try:
            self.check_input_path()
            self.check_output_dir()
        except FileNotFoundError as e:
            logging.error(str(e))
            raise

        # Validate and set window size
        try:
            self.window_size = self.check_positive_integer(window_size, "window size")
        except ValueError as e:
            logging.error(str(e))
            self.window_size = 1  # Set default only if window size is invalid
            logging.info("Default window size set to 1.")

        # Validate and set high value threshold
        try:
            self.high_value_threshold = self.check_positive_integer(high_value_threshold, "high value threshold")
        except ValueError as e:
            logging.error(str(e))
            self.high_value_threshold = 1  # Set default only if high value threshold is invalid
            logging.info("Default high value threshold set to 1.")

        self.band_number = band_number
        self.processor = GeoTIFFProcessor(input_path, output_dir, self.window_size, self.band_number,
                                          self.high_value_threshold)

    def run(self):
        """
        Runs the application driver.
        This method is responsible for starting the processing of the GeoTIFF file.
        It logs the start of the processing, the input and output paths, and the completion of the processing.

        """
        logging.info("Starting processing...")
        logging.info(f"Input path: {self.input_path}")
        logging.info(f"Output dir: {self.output_dir}")

        self.processor.process_tiff()

        logging.info("Processing completed.")

    @staticmethod
    def setup_logging():
        """
        Sets up logging configuration.
        The logging configuration is set to log all messages to a file named 'app.log' with the format:
            '%(asctime)s - %(levelname)s - %(name)s - %(message)s'.

        :return: None
        """
        logging.basicConfig(level=logging.DEBUG,  # Sets standard logging level to DEBUG
                            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                            filename='app.log',
                            filemode='w')
        logging.info("Logging is configured.")

    def check_input_path(self):
        """
        Checks if the input path is valid.
        If the input path is not valid, it logs an error message and raises a FileNotFoundError.

        :raises FileNotFoundError: If the input path is not valid.
        """
        if not os.path.isfile(self.input_path):
            logging.error(f"Invalid input path: {self.input_path}")
            raise FileNotFoundError(f"No file found at specified input path: {self.input_path}")
        logging.info(f"Valid input path: {self.input_path}")

    def check_output_dir(self):
        """
        Checks if the output directory exists.
        If the output directory does not exist, it logs an error message and raises a FileNotFoundError.

        :raises FileNotFoundError: If the output directory does not exist.
        """
        output_dir = os.path.dirname(self.output_dir)
        if not os.path.isdir(output_dir):
            logging.error(f"Invalid output directory: {output_dir}")
            raise FileNotFoundError(f"The directory for the output path does not exist: {output_dir}")
        logging.info(f"Valid output directory: {output_dir}")

    def check_positive_integer(self, value, parameter_name):
        """
        Validates that the given parameter is a positive integer.
        Raises ValueError if the validation fails.
        """
        if not isinstance(value, int) or value <= 0:
            raise ValueError(f"{parameter_name} must be a positive integer, got {value}.")
        logging.info(f"Valid {parameter_name}: {value}")
        return value

"""
application_driver.py
---------------------
Version: 1.1.0
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

from . import geo_tiff_processor
from .geo_tiff_processor import GeoTIFFProcessor


class ApplicationDriver:
    def __init__(self, input_path, output_dir, window_size=None, band_number=None, high_value_threshold=None,
                 categorical_thresholds=None):
        """
        Initializes the ApplicationDriver with the input and output paths.

        :param str input_path: The path to the input GeoTIFF file.
        :param str output_dir: The path to the output directory.
        :param float window_size: The side length of the square window in meters. Default is None.
        :param int band_number: The band number to be processed. Default is None.
        :param float high_value_threshold: The threshold for high values to be filtered out. Default is None.
        :param list categorical_thresholds: List of thresholds for categorizing data. Default is None.
        :raises FileNotFoundError: If the input path or output directory is not valid.
        """
        self.setup_logging()
        self.input_path = input_path
        self.output_dir = output_dir

        # Check required paths
        try:
            self.check_input_path()
            self.check_output_dir()
        except FileNotFoundError as e:
            logging.error(str(e))
            raise

        # Prepare parameters dictionary
        params = {
            'window_size': window_size if window_size is not None else None,
            'band_number': band_number if band_number is not None else None,
            'high_value_threshold': high_value_threshold if high_value_threshold is not None else None,
            'categorical_thresholds': categorical_thresholds if categorical_thresholds is not None else None
        }

        # Remove None values to avoid passing them to the processor
        filtered_params = {k: v for k, v in params.items() if v is not None}

        # Initialize the processor with filtered parameters
        self.processor = GeoTIFFProcessor(input_path, output_dir, **filtered_params)

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
                            filename='../app.log',
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

    def check_positive_number(self, value, parameter_name):
        """
        Validates that the given parameter is a positive number.
        Raises ValueError if the validation fails.
        """
        try:
            value = float(value)
            if value <= 0:
                raise ValueError(f"{parameter_name} must be a positive number, got {value}.")
        except ValueError:
            raise ValueError(f"{parameter_name} must be a positive number, got {value}.")
        logging.info(f"Valid {parameter_name}: {value}")
        return value

    def get_preview(self):
        """
        Retrieves the processed image from the GeoTIFFProcessor for display.
        :return: A PIL Image object of the processed TIFF data, or None if an error occurs.
        """
        try:
            image = self.processor.get_preview()
            if image:
                logging.info("Preview retrieved successfully.")
                return image
            else:
                logging.error("No preview could be retrieved.")
                return None
        except Exception as e:
            logging.error(f"Error retrieving preview: {str(e)}")
            return None

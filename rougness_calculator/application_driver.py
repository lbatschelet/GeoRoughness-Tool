# TODO: Add docstrings and comments

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
    def __init__(self, input_path, output_path):
        """
        Initializes the ApplicationDriver with the input and output paths.

        :param str input_path: The path to the input GeoTIFF file.
        :param str output_path: The path to the output GeoTIFF file.
        """
        self.setup_logging()
        self.input_path = input_path
        self.check_input_path()
        self.output_path = output_path
        self.check_output_path()
        self.processor = GeoTIFFProcessor(input_path, output_path)

    def run(self):
        """
        Runs the application driver.
        This method is responsible for starting the processing of the GeoTIFF file.
        It logs the start of the processing, the input and output paths, and the completion of the processing.

        """
        logging.info("Starting processing...")
        logging.info(f"Input path: {self.input_path}")
        logging.info(f"Output path: {self.output_path}")

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

    def check_output_path(self):
        """
        Checks if the output directory exists.
        If the output directory does not exist, it logs an error message and raises a FileNotFoundError.

        :raises FileNotFoundError: If the output directory does not exist.
        """
        output_dir = os.path.dirname(self.output_path)
        if not os.path.isdir(output_dir):
            logging.error(f"Invalid output directory: {output_dir}")
            raise FileNotFoundError(f"The directory for the output path does not exist: {output_dir}")
        logging.info(f"Valid output directory: {output_dir}")


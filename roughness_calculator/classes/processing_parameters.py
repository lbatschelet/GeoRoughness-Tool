"""
processing_parameters.py
---
Version: 1.1.0
Author: Lukas Batschelet
Date: 09.05.2024
---
Class to encapsulate the processing parameters for the surface roughness calculator application.
The used dataclass decorator is a Python 3.7 feature that allows for the creation of classes with
attributes and methods without the need for boilerplate code. The dataclass decorator automatically
generates special methods like __init__(), __repr__(), and __eq__() based on the attributes defined
in the class.
"""

from dataclasses import dataclass, field
import os
from typing import Optional, List

from .defaults import Defaults

import logging

import rasterio

logger = logging.getLogger(__name__)


@dataclass
class ProcessingParameters:
    """
    A class to encapsulate the processing parameters for an application,
    ensuring all parameters are validated and converted upon instantiation.

    Attributes:
        input_path (str): The path to the input file. Must be provided and must be a valid GeoTIFF.
        output_dir (Optional[str]): The directory where the output should be saved. Optional.
        window_size (float): The size of the window to use for processing. Defaults to 1.0.
        band_number (int): The specific band to process. Defaults to 1.
        high_value_threshold (float): Threshold for identifying high values. Defaults to 10.0.
        category_thresholds (Optional[List[float]]): List of thresholds for categorizing data. Optional.
    """
    input_path: str
    output_dir: Optional[str] = field(default_factory=lambda: Defaults.OUTPUT_DIR)
    window_size: float = field(default_factory=lambda: Defaults.WINDOW_SIZE)
    band_number: int = field(default_factory=lambda: Defaults.BAND_NUMBER)
    high_value_threshold: float = field(default_factory=lambda: Defaults.HIGH_VALUE_THRESHOLD)
    category_thresholds: Optional[List[float]] = field(default_factory=lambda: Defaults.CATEGORY_THRESHOLDS)

    def __post_init__(self):
        logger.info("Initializing ProcessingParameters...")

        # Validate input_path with updated method that raises exceptions
        self.validate_input_path(self.input_path)

        # Validate output_dir if provided
        if self.output_dir:
            self.validate_output_dir(self.output_dir)
        else:
            logger.info("No output directory provided.")

            # Validate band_number
        self.validate_band_number(self.input_path, self.band_number)

        if self.window_size <= 0:
            raise ValueError("Window size must be positive.")
        if self.high_value_threshold <= 0:
            raise ValueError("High value threshold must be positive.")

        # Validate and manage thresholds
        if self.category_thresholds:
            self.category_thresholds = self.sort_thresholds(self.category_thresholds)
            self.category_thresholds = self.check_max_threshold(self.category_thresholds, self.high_value_threshold)
            self.category_thresholds = self.check_positive_thresholds(self.category_thresholds)

    @classmethod
    def create_from_dict(cls, params: dict) -> "ProcessingParameters":
        """
        Factory method to create ProcessingParameters from a dictionary of parameters,
        performing all necessary validations and conversions.
        """
        input_path = params.get('input_path')
        output_dir = params.get('output_dir', Defaults.OUTPUT_DIR)
        window_size = float(params.get('window_size', Defaults.WINDOW_SIZE))
        band_number = int(params.get('band_number', Defaults.BAND_NUMBER))
        high_value_threshold = float(params.get('high_value_threshold', Defaults.HIGH_VALUE_THRESHOLD))
        category_thresholds = cls.convert_to_float_list(params.get('category_thresholds', Defaults.CATEGORY_THRESHOLDS))

        # Construct and return an instance with validated and converted parameters
        return cls(input_path, output_dir, window_size, band_number, high_value_threshold, category_thresholds)

    @staticmethod
    def validate_input_path(path: str) -> bool:
        """
        Validates that the input path is a valid GeoTIFF file.
        :param path: Path to the input file
        :return: bool indicating if the input path is valid
        """
        logger.debug("Validating input path...")
        if not os.path.exists(path):
            raise FileNotFoundError(f"The input path {path} does not exist.")
        if not os.path.isfile(path):
            raise ValueError(f"The input path {path} is not a file.")
        if not ProcessingParameters.is_tiff_file(path):
            raise ValueError(f"The input file {path} is not a GeoTIFF.")
        logger.info(f"Input path {path} is a valid GeoTIFF.")
        return True

    @staticmethod
    def is_tiff_file(filepath: str) -> bool:
        """
        Checks if the file at the given path is a valid GeoTIFF file.
        :param filepath: Path to the file to check
        :return: bool indicating if the file is a valid GeoTIFF
        """
        logger.debug(f"Checking if file is a valid GeoTIFF: {filepath}")
        try:
            with open(filepath, 'rb') as file:
                magic_number = file.read(4)
            if magic_number not in (b'II\x2A\x00', b'MM\x00\x2A'):
                logger.info("File does not have a valid TIFF magic number.")
                return False
            # Confirm with rasterio open
            with rasterio.open(filepath) as src:
                logger.info(f"TIFF file opened successfully with rasterio: {src.meta}")
            logger.info("File is a valid GeoTIFF.")
            return True
        except (IOError, rasterio.errors.RasterioIOError) as e:
            logger.error(f"Failed to open or process TIFF file: {e}")
            return False

    @staticmethod
    def validate_output_dir(path: str):
        """
        Validates that the output directory exists and is a directory.
        :param path: Path to the output directory
        :return: None
        """
        logger.debug("Validating output directory...")
        if not os.path.exists(path):
            raise FileNotFoundError(f"The output directory {path} does not exist.")
        if not os.path.isdir(path):
            raise ValueError(f"The output path {path} is not a directory.")
        logger.info(f"Output directory {path} is valid.")

    @staticmethod
    def convert_to_float_list(value_str: Optional[str]) -> Optional[List[float]]:
        """
        Converts a comma-separated string of values to a list of floats.
        :param value_str: Input string of comma-separated values
        :return: List of floats or None if the input is None
        """
        logger.debug("Converting string to float list...")
        if not value_str:
            logger.info("No category thresholds provided.")
            return None
        logger.info("String converted to float list.")
        return [float(x.strip()) for x in value_str.split(',')]

    @staticmethod
    def sort_thresholds(thresholds: List[float]) -> List[float]:
        """
        Sorts the category thresholds and logs a warning if they were not initially sorted.
        :param thresholds: List of thresholds to sort
        :return: Sorted list of thresholds
        """
        logger.debug("Sorting category thresholds...")
        sorted_thresholds = sorted(thresholds)
        if sorted_thresholds != thresholds:
            logger.warning("Category thresholds were not initially sorted.")
            logger.info(f"Sorted thresholds: {sorted_thresholds}")
        logger.info("Category thresholds are sorted.")
        return sorted_thresholds

    @staticmethod
    def check_max_threshold(thresholds: List[float], high_value_threshold: float) -> List[float]:
        """
        Removes thresholds that exceed the high value threshold and logs a warning.
        :param thresholds: List of thresholds to check
        :param high_value_threshold: singular threshold to compare against
        :return: List of valid thresholds
        """
        logger.debug("Checking max thresholds...")
        valid_thresholds = [t for t in thresholds if t < high_value_threshold]
        if len(valid_thresholds) != len(thresholds):
            logger.warning("Some thresholds exceeded the high value threshold and were removed.")
            logger.info(f"Valid thresholds: {valid_thresholds}")
        logger.info("All thresholds are below the high value threshold.")
        return valid_thresholds

    @staticmethod
    def check_positive_thresholds(thresholds: List[float]) -> List[float]:
        """
        Removes non-positive thresholds from the list and logs a warning.
        :param thresholds: List of thresholds to check if positive
        :return: List of positive thresholds
        """
        logger.debug("Checking positive thresholds...")
        valid_thresholds = [t for t in thresholds if t > 0]
        if len(valid_thresholds) != len(thresholds):
            logger.warning("Non-positive thresholds were removed.")
            logger.info(f"Valid thresholds: {valid_thresholds}")
        logger.info("All thresholds are positive.")
        return valid_thresholds

    @staticmethod
    def validate_band_number(path: str, band_number: int) -> bool:
        """
        Validates that the band number is within the valid range for the GeoTIFF file.
        :param path: Path to the GeoTIFF file
        :param band_number: Band number to validate
        :return: bool indicating if the band number is valid
        """
        logger.debug("Validating band number...")
        with rasterio.open(path) as src:
            if band_number < 1 or band_number > src.count:
                raise ValueError(f"The band number {band_number} is not valid for the GeoTIFF file {path}.")
        logger.info(f"Band number {band_number} is valid for the GeoTIFF file {path}.")
        return True

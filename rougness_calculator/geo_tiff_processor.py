"""
geo_tiff_processor.py
---------------------
Version: 1.0.0
Author: Lukas Batschelet
Date: 18.04.2024
---------------------
This module contains the GeoTIFFProcessor class which is responsible for processing GeoTIFF files.
It provides methods for loading, processing, and saving GeoTIFF files.
Until now, only a method to calculate the roughness of a GeoTIFF file has been implemented.
"""

import logging
import numpy as np
import rasterio

# Set up logging referring to the logger setup in application_driver.py
# This allows for consistent logging across the application
logger = logging.getLogger(__name__)


class GeoTIFFProcessor:
    """
    Main class in this module, responsible for processing GeoTIFF files
    .
    :var str input_path: The path to the input GeoTIFF file.
    :var str output_path: The path to the output GeoTIFF file.
    :var int window_size: The side length of the square window in meters for which to calculate roughness. Default 1
    :var int band_number: The band number to be processed. Default 1.
    :var int high_value_threshold: The threshold for high values to be filtered out. Default 1.
    :var rasterio.DatasetReader dataset: The rasterio dataset object representing the GeoTIFF file.
    """
    def __init__(self, input_path, output_path, window_size, band_number, high_value_threshold):
        self.input_path = input_path
        self.output_path = output_path
        self.window_size = window_size
        self.band_number = band_number
        self.high_value_threshold = high_value_threshold
        self.dataset = None

    def process_tiff(self):
        """
        Main method for processing the GeoTIFF file. Manages the processing workflow.
        Calls the necessary methods to load the file, calculate the roughness, and save the processed file.
        """
        self.load_tiff()
        if self.dataset:  # Check if the dataset was loaded successfully
            try:
                self.log_tiff_metadata()
                data = self.read_band()  # Reads band 1. Is set up to allow for future extension to read other bands.
                roughness = self.calculate_roughness(data)
                roughness = self.apply_nodata_and_filter(roughness)  # Filters out zero and high values at the border.
                self.save_tiff(roughness)
            finally:
                self.dataset.close()  # Close the dataset after processing
                logger.info("Processing completed and file closed")
        else:
            logger.error("Processing aborted due to failed file load.")

    def load_tiff(self):
        """
        Loads the GeoTIFF file into the dataset variable using rasterio.
        """
        if self.is_valid_tiff(self.input_path):
            self.dataset = rasterio.open(self.input_path, mode='r')
            logger.info("TIFF file loaded successfully.")

    def read_band(self):
        """
        Reads the specified band from the GeoTIFF file.
        :return: The data of the specified band.
        """
        return self.dataset.read(self.band_number)

    def calculate_roughness(self, data):
        """
        Calculates the roughness of the GeoTIFF file by dividing the image into windows of specified size in meters
        and calculating the standard deviation of heights within each window.

        :param data: Numpy array of raster data (elevation values).
        :return: A numpy array with the roughness values for each window.
        """
        pixel_width, pixel_height = self.get_pixel_size()
        pixels_per_window_x = int(round(self.window_size / pixel_width))
        pixels_per_window_y = int(round(self.window_size / pixel_height))
        new_height = data.shape[0] // pixels_per_window_y
        new_width = data.shape[1] // pixels_per_window_x
        roughness = np.empty((new_height, new_width))

        for i in range(new_height):
            for j in range(new_width):
                start_x = j * pixels_per_window_x
                start_y = i * pixels_per_window_y
                end_x = start_x + pixels_per_window_x
                end_y = start_y + pixels_per_window_y

                # Extract the window and calculate its standard deviation
                window = data[start_y:end_y, start_x:end_x]
                roughness[i, j] = np.std(window)

        return roughness

    @classmethod
    def is_valid_tiff(cls, filepath):
        """
        Checks if the file at the given path is a valid TIFF file.
        :param filepath:
        :return: True if the file is a valid TIFF file.
        :raise ValueError: If the file is not a valid TIFF file.
        """
        if not filepath:
            logger.error(f"No file selected for the path: {filepath}")
            raise ValueError("No file selected.")
        if not cls.is_tiff_file(filepath):
            logger.error(f"Invalid TIFF file selected: {filepath}")
            raise ValueError(f"Invalid TIFF file selected: {filepath}")

        logger.info(f"Valid TIFF file confirmed: {filepath}")
        return True

    @staticmethod
    def is_tiff_file(filepath):
        """
        Checks if the file at the given path is a TIFF file by reading the first 4 bytes of the file.

        :param filepath:
        :return: True if the file is a TIFF file, False otherwise.
        """
        try:
            with open(filepath, 'rb') as file:
                magic_number = file.read(4)
            # Checks for the TIFF magic number in little-endian and big-endian formats
            if magic_number not in (b'II\x2A\x00', b'MM\x00\x2A'):
                logger.info("File does not have a valid TIFF magic number.")
                return False
            with rasterio.open(filepath) as src:
                logger.info(f"TIFF file opened successfully with rasterio: {src.meta}")
            return True
        except (IOError, rasterio.errors.RasterioIOError) as e:
            logger.error(f"Failed to open or process TIFF file: {e}")
            return False

    def log_tiff_metadata(self):
        """
        Logs the metadata of the GeoTIFF file in 'app.log'
        :return: None
        """
        try:
            with rasterio.open(self.input_path) as src:
                logger.info(f"GeoTIFF metadata: {src.meta}")
        except rasterio.errors.RasterioIOError as e:
            logger.error(f"Failed to open GeoTIFF: {e}")
            raise ValueError(f"Invalid GeoTIFF file: {self.input_path}")

    def apply_nodata_and_filter(self, roughness, nodata_value=-9999):
        """
        Applies nodata value and filters out zero and high values that are created at the border of the roughness array.
        :param roughness:
        :param nodata_value: Default is -9999.
        :return: The roughness array with nodata values and filtered out zero and high values.
        """
        roughness[np.logical_or(roughness == 0, roughness > self.high_value_threshold)] = nodata_value
        return roughness

    def save_tiff(self, data, nodata=-9999, dtype='float32'):
        """
        Saves the processed TIFF file with the calculated roughness values.

        :param data: The processed data to be saved.
        :param nodata: The nodata value to be applied to the TIFF file. Default is -9999.
        :param dtype: The data type of the TIFF file. Default is 'float32'.
        :return: None
        """
        profile = self.dataset.profile
        profile.update(dtype=dtype, nodata=nodata)
        with rasterio.open(self.output_path, 'w', **profile) as dst:
            dst.write(data, 1)
        logger.info("Processed TIFF file saved.")

    def get_pixel_size(self):
        """
        Calculates the pixel size of the GeoTIFF file by extracting
        the pixel width and height from the transform attribute.

        :return: The pixel width and height of the GeoTIFF file.
        """
        transform = self.dataset.transform
        return transform[0], abs(transform[4])

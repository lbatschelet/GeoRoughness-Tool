"""
geo_tiff_processor.py
---------------------
Version: 1.1.0
Author: Lukas Batschelet
Date: 18.04.2024
---------------------
This module contains the GeoTIFFProcessor class which is responsible for processing GeoTIFF files.
It provides methods for loading, processing, and saving GeoTIFF files.
Until now, only a method to calculate the roughness of a GeoTIFF file has been implemented.
"""
import numpy as np
import rasterio
import logging
from ..log_config import setup_logging

# Ensure the logger is set up (optional if you know `log_config.py` is already imported elsewhere)
setup_logging()

logger = logging.getLogger(__name__)


class GeoTIFFProcessor:
    """
    Main class in this module, responsible for processing GeoTIFF files
    .
    :var str input_path: The path to the input GeoTIFF file.
    :var str output_dir: The path to the output directory.
    :var int window_size: The side length of the square window in meters for which to calculate roughness. Default 1
    :var int band_number: The band number to be processed. Default 1.
    :var int high_value_threshold: The threshold for high values to be filtered out. Default 1.
    :var rasterio.DatasetReader dataset: The rasterio dataset object representing the GeoTIFF file.
    """
    def __init__(self, input_path, window_size=1.0, band_number=1, high_value_threshold=1.0,
                 category_thresholds=None):

        self.input_path = input_path
        self.window_size = window_size
        self.band_number = band_number
        self.high_value_threshold = high_value_threshold
        self.category_thresholds = category_thresholds
        self.dataset = None
        self.processed_data = None
        self.profile = None

    def process_tiff(self):
        """
        Main method for processing the GeoTIFF file.
        Returns the processed data instead of saving it directly.
        """
        try:
            self.load_tiff()
            if not self.dataset:
                raise RuntimeError("TIFF dataset could not be opened.")

            self.log_tiff_metadata()
            data = self.read_band()
            processed_data = self.calculate_roughness(data)
            processed_data = self.apply_nodata(processed_data)
            processed_data = self.apply_filter(processed_data)

            if self.category_thresholds:
                processed_data = self.apply_thresholds(processed_data)
            self.processed_data = processed_data
            self.profile = self.dataset.profile  # Store profile before closing

            return processed_data
        except Exception as e:
            logging.error(f"An error occurred during processing: {e}")
            raise RuntimeError(f"An error occurred during processing: {e}")
        finally:
            if self.dataset:
                self.dataset.close()
                logging.info("Dataset closed successfully.")

    def load_tiff(self):
        """
        Loads the GeoTIFF file into the dataset variable using rasterio.
        """
        try:
            if not self.is_valid_tiff(self.input_path):
                logging.error(f"Invalid TIFF file: {self.input_path}")
                raise ValueError("Invalid TIFF file.")
            self.dataset = rasterio.open(self.input_path, mode='r')
            logging.info("TIFF file loaded successfully.")
        except rasterio.errors.RasterioIOError as e:
            logging.error(f"Failed to open TIFF file: {self.input_path}, {e}")
            raise RuntimeError(f"Failed to open TIFF file: {e}")

    def read_band(self):
        """
        Reads the specified band from the GeoTIFF file.
        :return: The data of the specified band.
        """
        if not self.dataset:
            logging.error("Attempted to read a band with no dataset loaded.")
            raise RuntimeError("Dataset not loaded.")
        try:
            data = self.dataset.read(self.band_number)
            logging.info(f"Band {self.band_number} read successfully.")
            return data
        except Exception as e:
            logging.error(f"Failed to read band {self.band_number}: {e}")
            raise

    def calculate_roughness(self, data):
        """
        Calculates the roughness of the GeoTIFF file by dividing the image into windows of specified size in meters
        and calculating the standard deviation of heights within each window.

        :param data: Numpy array of raster data (elevation values).
        :return: A numpy array with the roughness values for each window.
        """
        if data is None:
            logging.error("No data provided for roughness calculation.")
            raise ValueError("Data is required for roughness calculation.")

        try:
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
                    window = data[start_y:end_y, start_x:end_x]
                    roughness[i, j] = np.std(window)

            logging.info("Roughness calculated successfully.")
            return roughness
        except Exception as e:
            logging.error(f"Failed to calculate roughness: {str(e)}")
            raise

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

    def apply_filter(self, roughness, nodata_value=-9999):
        """
        Filters out too high values of the roughness array.
        :param roughness: The roughness array.
        :param nodata_value: Default is -9999.
        :return: The roughness array with high values filtered out.
        """
        if roughness is None:
            logging.error("No roughness data provided to filter.")
            raise ValueError("Roughness data is required for filtering.")
        roughness[roughness > self.high_value_threshold] = nodata_value
        logging.info("High values filtered from the roughness data.")
        return roughness

    def apply_nodata(self, roughness, nodata_value=-9999):
        """
        Applies nodata value and filters out zero and high values.
        :param roughness:
        :param nodata_value: Default is -9999.
        :return: The roughness array with nodata values and filtered out zero and high values.
        """
        if roughness is None:
            logging.error("No roughness data provided to apply nodata values.")
            raise ValueError("Roughness data is required for applying nodata values.")
        roughness[roughness == 0] = nodata_value
        logging.info("Nodata values applied to the roughness data.")
        return roughness

    def get_pixel_size(self):
        """
        Calculates the pixel size of the GeoTIFF file by extracting
        the pixel width and height from the transform attribute.

        :return: The pixel width and height of the GeoTIFF file.
        """
        if self.dataset is None:
            logging.error("No dataset loaded, cannot calculate pixel size.")
            raise RuntimeError("Dataset not loaded.")
        try:
            transform = self.dataset.transform
            pixel_size = (transform[0], abs(transform[4]))
            logging.info(f"Pixel size calculated: {pixel_size}")
            return pixel_size
        except AttributeError as e:
            logging.error("Error accessing transform of the dataset: " + str(e))
            raise

    def apply_thresholds(self, data, nodata_value=-9999):
        if self.category_thresholds is None or not self.category_thresholds:
            logging.error("No thresholds set for categorization.")
            raise ValueError("Category thresholds are not defined.")

        self.sort_thresholds()
        self.check_max_threshold()
        self.check_positive_thresholds()

        if data is None:
            logging.error("No data provided for threshold application.")
            raise ValueError("Data is required for applying thresholds.")

        valid_mask = data != nodata_value
        categorized_data = np.full(data.shape, nodata_value, dtype=data.dtype)

        for i, threshold in enumerate(self.category_thresholds):
            if i == 0:
                mask = (data > 0) & (data <= threshold) & valid_mask
            else:
                mask = (data > self.category_thresholds[i - 1]) & (data <= threshold) & valid_mask
            categorized_data[mask] = threshold

        high_value_mask = (data > self.category_thresholds[-1]) & (data <= self.high_value_threshold) & valid_mask
        categorized_data[high_value_mask] = self.high_value_threshold

        logging.info("Data categorized based on thresholds.")
        return categorized_data

    def sort_thresholds(self):
        if self.category_thresholds is not None:
            if sorted(self.category_thresholds) != self.category_thresholds:
                self.category_thresholds.sort()
                raise ValueError("Thresholds were not sorted. They have been sorted now.")

    def check_max_threshold(self):
        if self.category_thresholds and max(self.category_thresholds) >= self.high_value_threshold:
            self.category_thresholds = [th for th in self.category_thresholds if th < self.high_value_threshold]
            raise ValueError("Some thresholds exceeded the high value threshold and were removed.")

    def check_positive_thresholds(self):
        if self.category_thresholds and any(th <= 0 for th in self.category_thresholds):
            self.category_thresholds = [th for th in self.category_thresholds if th > 0]
            raise ValueError("Non-positive thresholds were removed.")

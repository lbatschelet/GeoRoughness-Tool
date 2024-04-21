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
from typing import Optional, List, Tuple

# Ensure the logger is set up (optional if you know `log_config.py` is already imported elsewhere)
setup_logging()

logger = logging.getLogger(__name__)


class GeoTIFFProcessor:
    """
    Main class in this module, responsible for processing GeoTIFF files.

    Attributes:
        input_path (str): The path to the input GeoTIFF file.
        window_size (float): The side length of the square window in meters for which to calculate roughness. Default 1
        band_number (int): The band number to be processed. Default 1.
        high_value_threshold (float): The threshold for high values to be filtered out. Default 1.
        category_thresholds (Optional[List[float]]): The thresholds for categorizing the roughness values.
        dataset (Optional[rasterio.DatasetReader]): The rasterio dataset object representing the GeoTIFF file.
        processed_data (Optional[np.ndarray]): The processed data.
        profile (Optional[Dict]): The profile of the GeoTIFF file.
    """
    def __init__(self, input_path: str, window_size: float = 1.0, band_number: int = 1,
                 high_value_threshold: float = 1.0, category_thresholds: Optional[List[float]] = None) -> None:
        """
        Initializes the GeoTIFFProcessor with the given parameters.

        Args:
            input_path (str): The path to the input GeoTIFF file.
            window_size (float, optional): The side length of the square window in meters for which to calculate
                                           roughness. Defaults to 1.0.
            band_number (int, optional): The band number to be processed. Defaults to 1.
            high_value_threshold (float, optional): The threshold for high values to be filtered out. Defaults to 1.0.
            category_thresholds (Optional[List[float]], optional): The thresholds for categorizing the roughness values.
                                                                   Defaults to None.
        """
        # Store the input parameters
        self.input_path = input_path
        self.window_size = window_size
        self.band_number = band_number
        self.high_value_threshold = high_value_threshold
        self.category_thresholds = category_thresholds

        # Initialize the dataset, processed_data, and profile attributes to None
        self.dataset = None
        self.processed_data = None
        self.profile = None

    def process_tiff(self) -> np.ndarray:
        """
        Main method for processing the GeoTIFF file.
        Returns the processed data instead of saving it directly.

        This method loads the GeoTIFF file, logs its metadata, reads the specified band, calculates the roughness,
        applies nodata values, filters out high values, and applies thresholds if they are defined.
        The processed data and the profile of the GeoTIFF file are stored in the instance variables.

        Returns:
            np.ndarray: The processed data.

        Raises:
            RuntimeError: If the TIFF dataset could not be opened, or an error occurred during processing.
        """
        try:
            # Load the GeoTIFF file
            self.load_tiff()
            # Raise an error if the dataset could not be opened
            if not self.dataset:
                raise RuntimeError("TIFF dataset could not be opened.")

            # Log the metadata of the GeoTIFF file
            self.log_tiff_metadata()
            # Read the specified band from the GeoTIFF file
            data = self.read_band()
            # Calculate the roughness of the GeoTIFF file
            processed_data = self.calculate_roughness(data)
            # Apply nodata values to the roughness data
            processed_data = self.apply_nodata(processed_data)
            # Filter out high values from the roughness data
            processed_data = self.apply_filter(processed_data)

            # If thresholds are defined, apply them to the roughness data
            if self.category_thresholds:
                processed_data = self.apply_thresholds(processed_data)
            # Store the processed data and the profile of the GeoTIFF file
            self.processed_data = processed_data
            self.profile = self.dataset.profile  # Store profile before closing

            # Return the processed data
            return processed_data
        except Exception as e:
            # Log the error and raise a new error
            logging.error(f"An error occurred during processing: {e}")
            raise RuntimeError(f"An error occurred during processing: {e}")
        finally:
            # If the dataset is loaded, close it and log a confirmation message
            if self.dataset:
                self.dataset.close()
                logging.info("Dataset closed successfully.")

    def load_tiff(self) -> None:
        """
        Loads the GeoTIFF file into the dataset variable using rasterio.

        This method attempts to open the GeoTIFF file at the specified input path using rasterio.
        If the file is not a valid TIFF file, it logs an error message and raises a ValueError.
        If the file is a valid TIFF file, it logs a confirmation message and stores the rasterio dataset object in the
        dataset attribute.

        Raises:
            ValueError: If the file is not a valid TIFF file.
            RuntimeError: If the file could not be opened with rasterio.
        """
        try:
            # Check if the file at the input path is a valid TIFF file
            if not self.is_valid_tiff(self.input_path):
                # If the file is not a valid TIFF file, log an error message
                logging.error(f"Invalid TIFF file: {self.input_path}")
                # Raise a ValueError with a descriptive error message
                raise ValueError("Invalid TIFF file.")
            # If the file is a valid TIFF file, open it with rasterio and store the
            # dataset object in the dataset attribute
            self.dataset = rasterio.open(self.input_path, mode='r')
            # Log a confirmation message
            logging.info("TIFF file loaded successfully.")
        except rasterio.errors.RasterioIOError as e:
            # If the file could not be opened with rasterio, log an error message
            logging.error(f"Failed to open TIFF file: {self.input_path}, {e}")
            # Raise a RuntimeError with a descriptive error message
            raise RuntimeError(f"Failed to open TIFF file: {e}")

    def read_band(self) -> np.ndarray:
        """
        Reads the specified band from the GeoTIFF file.

        This method attempts to read the specified band from the GeoTIFF file using the rasterio dataset object.
        If the dataset object is not loaded, it logs an error message and raises a RuntimeError.
        If the band is successfully read, it logs a confirmation message and returns the data of the band.
        If an error occurs during the reading process, it logs an error message and raises the original exception.

        Returns:
            np.ndarray: The data of the specified band.

        Raises:
            RuntimeError: If the dataset object is not loaded.
            Exception: If an error occurs during the reading process.
        """
        # Check if the dataset object is loaded
        if not self.dataset:
            # If the dataset object is not loaded, log an error message
            logging.error("Attempted to read a band with no dataset loaded.")
            # Raise a RuntimeError with a descriptive error message
            raise RuntimeError("Dataset not loaded.")
        try:
            # Attempt to read the specified band from the GeoTIFF file
            data = self.dataset.read(self.band_number)
            # Log a confirmation message
            logging.info(f"Band {self.band_number} read successfully.")
            # Return the data of the band
            return data
        except Exception as e:
            # If an error occurs during the reading process, log an error message
            logging.error(f"Failed to read band {self.band_number}: {e}")
            # Raise the original exception
            raise

    def calculate_roughness(self, data: np.ndarray) -> np.ndarray:
        """
        Calculates the roughness of the GeoTIFF file.

        This method divides the image into windows of specified size in meters and calculates the standard deviation of
        heights within each window. The roughness is calculated as the standard deviation of the elevation values within
        each window.

        Args:
            data (np.ndarray): Numpy array of raster data (elevation values).

        Returns:
            np.ndarray: A numpy array with the roughness values for each window.

        Raises:
            ValueError: If no data is provided for roughness calculation.
            Exception: If an error occurs during the roughness calculation.
        """
        # Check if data is provided
        if data is None:
            logging.error("No data provided for roughness calculation.")
            raise ValueError("Data is required for roughness calculation.")

        try:
            # Calculate the pixel size
            pixel_width, pixel_height = self.get_pixel_size()
            # Calculate the number of pixels per window in x and y directions
            pixels_per_window_x = int(round(self.window_size / pixel_width))
            pixels_per_window_y = int(round(self.window_size / pixel_height))
            # Calculate the new height and width of the roughness array
            new_height = data.shape[0] // pixels_per_window_y
            new_width = data.shape[1] // pixels_per_window_x
            # Initialize the roughness array
            roughness = np.empty((new_height, new_width))

            # Loop over the windows in the data array
            for i in range(new_height):
                for j in range(new_width):
                    # Calculate the start and end indices of the window in x and y directions
                    start_x = j * pixels_per_window_x
                    start_y = i * pixels_per_window_y
                    end_x = start_x + pixels_per_window_x
                    end_y = start_y + pixels_per_window_y
                    # Extract the window from the data array
                    window = data[start_y:end_y, start_x:end_x]
                    # Calculate the standard deviation of the window and store it in the roughness array
                    roughness[i, j] = np.std(window)

            # Log a confirmation message
            logging.info("Roughness calculated successfully.")
            # Return the roughness array
            return roughness
        except Exception as e:
            # If an error occurs during the roughness calculation, log an error message
            logging.error(f"Failed to calculate roughness: {str(e)}")
            # Raise the original exception
            raise

    @classmethod
    def is_valid_tiff(cls, filepath: str) -> bool:
        """
        Checks if the file at the given path is a valid TIFF file.

        This method first checks if a file path is provided. If not, it logs an error message and raises a ValueError.
        Then, it checks if the file at the given path is a TIFF file by calling the `is_tiff_file` method.
        If the file is not a TIFF file, it logs an error message and raises a ValueError.
        If the file is a TIFF file, it logs a confirmation message and returns True.

        Args:
            filepath (str): The path to the file to be checked.

        Returns:
            bool: True if the file is a valid TIFF file, False otherwise.

        Raises:
            ValueError: If no file path is provided or the file is not a valid TIFF file.
        """
        # Check if a file path is provided
        if not filepath:
            # If not, log an error message
            logger.error(f"No file selected for the path: {filepath}")
            # Raise a ValueError with a descriptive error message
            raise ValueError("No file selected.")
        # Check if the file at the given path is a TIFF file
        if not cls.is_tiff_file(filepath):
            # If the file is not a TIFF file, log an error message
            logger.error(f"Invalid TIFF file selected: {filepath}")
            # Raise a ValueError with a descriptive error message
            raise ValueError(f"Invalid TIFF file selected: {filepath}")

        # If the file is a TIFF file, log a confirmation message
        logger.info(f"Valid TIFF file confirmed: {filepath}")
        # Return True
        return True

    @staticmethod
    def is_tiff_file(filepath: str) -> bool:
        """
        Checks if the file at the given path is a TIFF file by reading the first 4 bytes of the file.

        This method attempts to open the file at the given path in binary mode and read the first 4 bytes.
        It checks if these bytes match the magic number for TIFF files in both little-endian and big-endian formats.
        If the file is a TIFF file, it logs a confirmation message and returns True.
        If the file is not a TIFF file or an error occurs during the process,
        it logs an error message and returns False.

        Args:
            filepath (str): The path to the file to be checked.

        Returns:
            bool: True if the file is a TIFF file, False otherwise.
        """
        try:
            # Open the file at the given path in binary mode
            with open(filepath, 'rb') as file:
                # Read the first 4 bytes of the file
                magic_number = file.read(4)
            # Check if these bytes match the magic number for TIFF files in both little-endian and big-endian formats
            if magic_number not in (b'II\x2A\x00', b'MM\x00\x2A'):
                # If the file is not a TIFF file, log an info message
                logger.info("File does not have a valid TIFF magic number.")
                # Return False
                return False
            # If the file is a TIFF file, open it with rasterio and log a confirmation message
            with rasterio.open(filepath) as src:
                logger.info(f"TIFF file opened successfully with rasterio: {src.meta}")
            # Return True
            return True
        except (IOError, rasterio.errors.RasterioIOError) as e:
            # If an error occurs during the process, log an error message
            logger.error(f"Failed to open or process TIFF file: {e}")
            # Return False
            return False

    def log_tiff_metadata(self) -> None:
        """
        Logs the metadata of the GeoTIFF file.

        This method attempts to open the GeoTIFF file at the specified input path using rasterio.
        If the file is successfully opened, it logs the metadata of the GeoTIFF file.
        If an error occurs during the process, it logs an error message and raises a ValueError.

        Raises:
            ValueError: If the file could not be opened with rasterio.
        """
        try:
            with rasterio.open(self.input_path) as src:
                logger.info(f"GeoTIFF metadata: {src.meta}")
        except rasterio.errors.RasterioIOError as e:
            logger.error(f"Failed to open GeoTIFF: {e}")
            raise ValueError(f"Invalid GeoTIFF file: {self.input_path}")

    def apply_filter(self, roughness: np.ndarray, nodata_value: int = -9999) -> np.ndarray:
        """
        Filters out high values from the roughness array.

        This method replaces values in the roughness array that are greater than the high value
        threshold with a nodata value.

        Args:
            roughness (np.ndarray): The roughness array.
            nodata_value (int, optional): The value to replace high values with. Defaults to -9999.

        Returns:
            np.ndarray: The roughness array with high values replaced by the nodata value.

        Raises:
            ValueError: If no roughness data is provided.
        """
        if roughness is None:
            logging.error("No roughness data provided to filter.")
            raise ValueError("Roughness data is required for filtering.")

        roughness[roughness > self.high_value_threshold] = nodata_value
        logging.info("High values filtered from the roughness data.")

        return roughness

    def apply_nodata(self, roughness: np.ndarray, nodata_value: int = -9999) -> np.ndarray:
        """
        Applies nodata value and filters out zero values from the roughness array.

        This method replaces zero values in the roughness array with a nodata value.

        Args:
            roughness (np.ndarray): The roughness array.
            nodata_value (int, optional): The value to replace zero values with. Defaults to -9999.

        Returns:
            np.ndarray: The roughness array with zero values replaced by the nodata value.

        Raises:
            ValueError: If no roughness data is provided.
        """
        # Check if roughness data is provided
        if roughness is None:
            logging.error("No roughness data provided to apply nodata values.")
            raise ValueError("Roughness data is required for applying nodata values.")

        # Replace zero values in the roughness array with the nodata value
        roughness[roughness == 0] = nodata_value
        logging.info("Nodata values applied to the roughness data.")

        # Return the modified roughness array
        return roughness

    def get_pixel_size(self) -> Tuple[float, float]:
        """
        Calculates the pixel size of the GeoTIFF file.

        This method extracts the pixel width and height from the transform attribute of the dataset.

        Returns:
            Tuple[float, float]: The pixel width and height of the GeoTIFF file.

        Raises:
            RuntimeError: If the dataset is not loaded.
            AttributeError: If there's an error accessing the transform of the dataset.
        """
        # Check if the dataset is loaded
        if self.dataset is None:
            logging.error("No dataset loaded, cannot calculate pixel size.")
            raise RuntimeError("Dataset not loaded.")

        try:
            # Extract the transform attribute from the dataset
            transform = self.dataset.transform
            # Calculate the pixel size
            pixel_size = (transform[0], abs(transform[4]))
            logging.info(f"Pixel size calculated: {pixel_size}")
            # Return the pixel size
            return pixel_size
        except AttributeError as e:
            # Log the error and raise the original exception
            logging.error("Error accessing transform of the dataset: " + str(e))
            raise

    def apply_thresholds(self, data: np.ndarray, nodata_value: int = -9999) -> np.ndarray:
        """
        Applies thresholds to the data array.

        This method replaces values in the data array that are within certain ranges defined by the category thresholds
        with the corresponding threshold value. Values greater than the highest threshold and less than or equal to the
        high value threshold are replaced with the high value threshold.

        Args:
            data (np.ndarray): The data array.
            nodata_value (int, optional): The value to replace nodata values with. Defaults to -9999.

        Returns:
            np.ndarray: The data array with values replaced based on the thresholds.

        Raises:
            ValueError: If no data is provided or if category thresholds are not defined.
        """
        # Check if category thresholds are defined
        if self.category_thresholds is None or not self.category_thresholds:
            logging.error("No thresholds set for categorization.")
            raise ValueError("Category thresholds are not defined.")

        # Check if data is provided
        if data is None:
            logging.error("No data provided for threshold application.")
            raise ValueError("Data is required for applying thresholds.")

        # Create a mask for valid data values
        valid_mask = data != nodata_value
        # Initialize the categorized data array with nodata values
        categorized_data = np.full(data.shape, nodata_value, dtype=data.dtype)

        # Loop over the category thresholds
        for i, threshold in enumerate(self.category_thresholds):
            # Create a mask for values within the current threshold range
            if i == 0:
                mask = (data > 0) & (data <= threshold) & valid_mask
            else:
                mask = (data > self.category_thresholds[i - 1]) & (data <= threshold) & valid_mask
            # Replace values within the current threshold range with the threshold value
            categorized_data[mask] = threshold

        # Create a mask for values within the high value range
        high_value_mask = (data > self.category_thresholds[-1]) & (data <= self.high_value_threshold) & valid_mask
        # Replace values within the high value range with the high value threshold
        categorized_data[high_value_mask] = self.high_value_threshold

        logging.info("Data categorized based on thresholds.")
        return categorized_data

    def sort_thresholds(self) -> None:
        """
        Sorts the category thresholds in ascending order.

        This method checks if the category thresholds are defined and not already sorted.
        If they are not sorted, it sorts them and raises a ValueError.

        Raises:
            ValueError: If the category thresholds were not sorted.
        """
        # Check if category thresholds are defined
        if self.category_thresholds is not None:
            # Check if category thresholds are not sorted
            if sorted(self.category_thresholds) != self.category_thresholds:
                # Sort the category thresholds
                self.category_thresholds.sort()
                # Raise a ValueError indicating that the thresholds were not sorted
                raise ValueError("Thresholds were not sorted. They have been sorted now.")

    def check_max_threshold(self) -> None:
        """
        Checks if any category threshold exceeds the high value threshold.

        This method checks if the category thresholds are defined and if any of them exceed the high value threshold.
        If any threshold exceeds the high value threshold, it removes it and raises a ValueError.

        Raises:
            ValueError: If some thresholds exceeded the high value threshold and were removed.
        """
        # Check if category thresholds are defined
        if self.category_thresholds:
            # Check if any category threshold exceeds the high value threshold
            if max(self.category_thresholds) >= self.high_value_threshold:
                # Remove thresholds that exceed the high value threshold
                self.category_thresholds = [th for th in self.category_thresholds if th < self.high_value_threshold]
                # Raise a ValueError indicating that some thresholds exceeded the high value threshold and were removed
                raise ValueError("Some thresholds exceeded the high value threshold and were removed.")

    def check_positive_thresholds(self) -> None:
        """
        Checks if any category threshold is non-positive.

        This method checks if the category thresholds are defined and if any of them are non-positive.
        If any threshold is non-positive, it removes it and raises a ValueError.

        Raises:
            ValueError: If non-positive thresholds were removed.
        """
        # Check if category thresholds are defined
        if self.category_thresholds:
            # Check if any category threshold is non-positive
            if any(th <= 0 for th in self.category_thresholds):
                # Remove non-positive thresholds
                self.category_thresholds = [th for th in self.category_thresholds if th > 0]
                # Raise a ValueError indicating that non-positive thresholds were removed
                raise ValueError("Non-positive thresholds were removed.")

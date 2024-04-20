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
import datetime
import logging
import os

import numpy as np
import rasterio
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib import cm

# Set up logging referring to the logger setup in application_driver.py
# This allows for consistent logging across the application
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
    def __init__(self, input_path, output_dir, window_size=1.0, band_number=1, high_value_threshold=1.0,
                 category_thresholds=None):

        self.input_path = input_path
        self.output_dir = output_dir
        self.window_size = window_size
        self.band_number = band_number
        self.high_value_threshold = high_value_threshold
        self.category_thresholds = category_thresholds
        self.output_path = self.create_output_filename()
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
                data = self.read_band()  # Reads the specified band.
                roughness = self.calculate_roughness(data)
                roughness = self.apply_nodata(roughness)  # Apply nodata filter first to reset invalid values.
                roughness = self.apply_filter(roughness)  # Then apply high value threshold filter.
                if self.category_thresholds:
                    roughness = self.apply_thresholds(roughness)  # Apply categorical thresholds last.
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

    def apply_filter(self, roughness, nodata_value=-9999):
        """
        Filters out too high values of the roughness array.
        Most high values are caused by not rectangular tiff files, thus leading to any value to 0 elevation changes.
        :param roughness: The roughness array.
        :return: The roughness array with high values filtered out.
        """
        roughness[roughness > self.high_value_threshold] = nodata_value
        return roughness

    def apply_nodata(self, roughness, nodata_value=-9999):
        """
        Applies nodata value and filters out zero and high values that are created at the border of the roughness array.
        :param roughness:
        :param nodata_value: Default is -9999.
        :return: The roughness array with nodata values and filtered out zero and high values.
        """
        roughness[roughness == 0] = nodata_value
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
        logging.info(f"Processed TIFF file saved at {self.output_path}")

    def get_pixel_size(self):
        """
        Calculates the pixel size of the GeoTIFF file by extracting
        the pixel width and height from the transform attribute.

        :return: The pixel width and height of the GeoTIFF file.
        """
        transform = self.dataset.transform
        return transform[0], abs(transform[4])

    def create_output_filename(self):
        """
        Generates a filename based on the input file, current date, and processing parameters.
        """
        # Extract the base name of the input file and remove the extension
        base_name = os.path.splitext(os.path.basename(self.input_path))[0]
        # Get current date in YYYYMMDD format
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        # Construct the new filename
        new_filename = f"{current_date}_{base_name}_Surface-Roughness_{self.window_size}-meter.tif"
        # Construct the full output path
        return os.path.join(self.output_dir, new_filename)

    def get_preview(self):
        """
        Loads the processed TIFF file, applies a pseudocolor colormap, and converts it to a PIL Image as preview for
        display in the GUI, with nodata values made transparent.
        :return: PIL Image object preview of the processed TIFF file in a pseudocolored format.
        """
        try:
            with rasterio.open(self.output_path, mode='r') as dataset:  # Open the processed TIFF file
                data = dataset.read(1)  # Assuming band 1 contains the roughness data
                nodata_value = dataset.nodatavals[0]  # Retrieve the nodata value from the dataset

                # Normalize the data for color mapping
                valid_mask = data != nodata_value
                scaled_data = np.ma.masked_equal(data, nodata_value)  # Mask out nodata values
                normalized_data = (scaled_data - scaled_data.min()) / (scaled_data.max() - scaled_data.min())

                # Create an RGBA image where nodata values are set to be transparent
                rgba_image = np.zeros((data.shape[0], data.shape[1], 4), dtype=np.uint8)
                color_mapped = plt.cm.viridis(normalized_data)  # Apply colormap
                rgba_image[..., :3] = (color_mapped[..., :3] * 255).astype(np.uint8)  # Set RGB channels
                rgba_image[..., 3] = (valid_mask * 255).astype(np.uint8)  # Set alpha channel: transparent if nodata

                preview = Image.fromarray(rgba_image, 'RGBA')
                return preview

        except Exception as e:
            logger.error(f"Failed to load or process TIFF file for display: {str(e)}")
            return None

    def apply_thresholds(self, data, nodata_value=-9999):
        self.sort_thresholds()
        self.check_max_threshold()
        self.check_positive_thresholds()

        valid_mask = data != nodata_value
        categorized_data = np.full(data.shape, nodata_value, dtype=data.dtype)  # Behalte dtype von data

        # Ordne jeden Wert der entsprechenden Kategorie zu, weise den Schwellenwert zu
        for i, threshold in enumerate(self.category_thresholds):
            if i == 0:
                # Behandle den ersten Bereich
                mask = (data > 0) & (data <= threshold) & valid_mask
            else:
                # Behandle alle anderen Bereiche
                mask = (data > self.category_thresholds[i - 1]) & (data <= threshold) & valid_mask
            categorized_data[mask] = threshold

        # Behandle Werte, die größer als der höchste Schwellenwert sind, aber unter oder gleich dem high_value_threshold
        high_value_mask = (data > self.category_thresholds[-1]) & (data <= self.high_value_threshold) & valid_mask
        categorized_data[high_value_mask] = self.high_value_threshold

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

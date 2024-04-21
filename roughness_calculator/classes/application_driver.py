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
from typing import List, Optional
import datetime
import os

import numpy as np
import rasterio
from PIL import Image
import matplotlib.pyplot as plt

from .geo_tiff_processor import GeoTIFFProcessor

import logging
from ..log_config import setup_logging

# Ensure the logger is set up (optional if you know `log_config.py` is already imported elsewhere)
setup_logging()

logger = logging.getLogger(__name__)


class ApplicationDriver:
    def __init__(
            self,
            input_path: str,
            output_dir: Optional[str] = None,
            window_size: Optional[float] = None,
            band_number: Optional[int] = None,
            high_value_threshold: Optional[float] = None,
            categorical_thresholds: Optional[List[float]] = None
    ):
        """
        Initializes the ApplicationDriver with necessary parameters for processing a GeoTIFF file.

        Args:
            input_path (str): Path to the input GeoTIFF file.
            output_dir (str, optional): Path to the output directory. If None, data is processed but not saved.
            window_size (float, optional): Side length of the square window in meters for roughness calculation.
            band_number (int, optional): Specific band number to process.
            high_value_threshold (float, optional): Threshold value to filter out high data values.
            categorical_thresholds (List[float], optional): Thresholds for categorizing data values.

        Raises:
            FileNotFoundError: If the input path or output directory is not valid.
        """

        self.input_path = input_path  # Store the path to the input GeoTIFF file
        self.output_dir = output_dir  # Store the path to the output directory if provided

        # Attempt to create an output filename if an output directory is provided
        self.output_path = self.create_output_filename() if output_dir else None

        # Store additional processing parameters
        self.window_size = window_size
        self.band_number = band_number
        self.high_value_threshold = high_value_threshold
        self.categorical_thresholds = categorical_thresholds

        self.processed_data = None  # This will hold the processed data after running the processor
        self.preview = None  # This will hold the image preview of the processed data

        # Validate the input path and output directory if provided
        self.check_input_path()
        if output_dir:
            self.check_output_dir()

        # Create a dictionary of processing parameters, excluding None values
        params = {
            'window_size': window_size,
            'band_number': band_number,
            'high_value_threshold': high_value_threshold,
            'categorical_thresholds': categorical_thresholds
        }
        filtered_params = {k: v for k, v in params.items() if v is not None}

        # Initialize the GeoTIFFProcessor with filtered parameters
        self.processor = GeoTIFFProcessor(input_path, **filtered_params)

    def run(self):
        """
        Runs the application driver.
        This method is responsible for starting the processing of the GeoTIFF file.
        It logs the start of the processing, the input and output paths, and the completion of the processing.

        """
        logging.info("Starting processing...")
        logging.info(f"Input path: {self.input_path}")
        logging.info(f"Output dir: {self.output_dir}")

        self.processed_data = self.processor.process_tiff()
        if self.output_dir:  # Wenn im CLI-Modus ausgeführt, speichere sofort.
            self.save_processed_data(self.processed_data)
        else:
            self.produce_preview()

        logging.info("Processing completed.")

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

    def produce_preview(self, nodata_value=-9999):
        """
        Generates a preview image from the processed data stored in self.processed_data.
        This method avoids re-reading the data from file, making it more efficient.
        Uses pseudocolor to represent the data visually, ensuring nodata values are transparent.
        """
        try:
            if self.processed_data is None:
                logging.error("No processed data available for preview.")
                raise ValueError("Processed data is not available for preview.")

            # Assuming nodata values are set correctly in the processor
            logging.debug(f"Using nodata value: {nodata_value}")

            # Normalize the data for color mapping
            valid_mask = self.processed_data != nodata_value
            masked_data = np.ma.masked_equal(self.processed_data, nodata_value)
            if masked_data.count() == 0:
                logging.error("All data are nodata. Cannot generate a preview.")
                raise ValueError("All data are nodata. Cannot generate a preview.")

            normalized_data = (masked_data - masked_data.min()) / (masked_data.max() - masked_data.min())

            # Create an RGBA image where nodata values are set to be transparent
            rgba_image = np.zeros((self.processed_data.shape[0], self.processed_data.shape[1], 4), dtype=np.uint8)
            color_mapped = plt.cm.viridis(normalized_data)  # Apply colormap
            rgba_image[..., :3] = (color_mapped[..., :3] * 255).astype(np.uint8)
            rgba_image[..., 3] = (valid_mask * 255).astype(np.uint8)  # Set alpha channel to transparent if nodata

            self.preview = Image.fromarray(rgba_image, 'RGBA')
            logging.info("Preview generated successfully.")
        except Exception as e:
            logging.error(f"Failed to produce preview: {str(e)}")
            self.preview = None
            raise RuntimeError("Failed to produce preview due to an error.") from e

    def save_processed_data(self, output_path, nodata=-9999, dtype='float32'):
        """
        Saves the processed data using the stored profile.
        """
        if self.processed_data is None or self.processor.profile is None:
            logging.error("Processed data or profile is not available for saving.")
            raise ValueError("Processed data or profile is missing.")

        self.processor.profile.update(dtype=dtype, nodata=nodata)
        with rasterio.open(output_path, 'w', **self.processor.profile) as dst:
            dst.write(self.processed_data, 1)
        logging.info(f"Processed data saved to {output_path}")

    def create_output_filename(self):
        """
        Generates a filename based on the input file, current date, and processing parameters.
        """
        base_name = os.path.splitext(os.path.basename(self.input_path))[0]
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        new_filename = f"{current_date}_{base_name}_Surface-Roughness_{self.window_size}-meter.tif"
        return os.path.join(self.output_dir, new_filename)

    def get_preview(self):
        """
        Retrieves the generated preview if available.
        Raises an exception if the preview is not available.
        """
        if self.preview is not None:
            return self.preview
        else:
            error_message = "Preview is not available or failed to generate."
            logging.error(error_message)
            raise RuntimeError(error_message)

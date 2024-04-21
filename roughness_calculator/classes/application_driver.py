"""
application_driver.py
---------------------
Version: 1.0.5
Author: Lukas Batschelet
Date: 21.04.2024
---------------------
This module contains the ApplicationDriver class which is responsible for running the application.
It acts as a sort of interface between the calling User Interface (UI) and the GeoTIFFProcessor class.
This enables the separation of concerns and allows for easier testing and maintenance of the code.
(i.e. the UI does not need to know how the processing is done, it just needs to know how to call the processing.)
"""
from typing import List, Optional, Union
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


def check_positive_number(value: Union[int, float], parameter_name: str) -> float:
    """
    Validates that the given parameter is a positive number.

    This function attempts to convert the input value to a float and checks if it is a positive number.
    If the value is not a positive number, it raises a ValueError with a descriptive error message.
    If the value is a positive number, it logs a confirmation message and returns the value.

    Args:
        value (Union[int, float]): The value to be checked.
        parameter_name (str): The name of the parameter, used in error messages.

    Returns:
        float: The validated value, guaranteed to be a positive number.

    Raises:
        ValueError: If the value is not a positive number or cannot be converted to a float.
    """
    try:
        # Attempt to convert the value to a float
        value = float(value)
        # If the value is not a positive number, raise a ValueError
        if value <= 0:
            raise ValueError(f"{parameter_name} must be a positive number, got {value}.")
    except ValueError:
        # If the value cannot be converted to a float, raise a ValueError
        raise ValueError(f"{parameter_name} must be a positive number, got {value}.")
    # If the value is a positive number, log a confirmation message
    logging.info(f"Valid {parameter_name}: {value}")

    return value


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

    def run(self) -> None:
        """
        Initiates the processing of the GeoTIFF file.

        This method is responsible for initiating the processing of the GeoTIFF file. It logs the start and end of the
        processing, as well as the input and output paths. If an output directory is provided,
        it saves the processed data immediately. Otherwise, it generates a preview of the processed data.

        Raises:
            ValueError: If the processed data is not available for saving or preview generation.
            RuntimeError: If there is an error during the saving or preview generation process.
        """
        # Log the start of the processing
        logging.info("Starting processing...")
        logging.info(f"Input path: {self.input_path}")
        logging.info(f"Output dir: {self.output_dir}")

        # Process the GeoTIFF file and store the result in self.processed_data
        self.processed_data = self.processor.process_tiff()

        # If an output directory is provided or running in CLI mode, save the processed data immediately
        if self.output_dir:
            self.save_processed_data(self.processed_data)

        # Otherwise, generate a preview of the processed data
        else:
            self.produce_preview()

        logging.info("Processing completed.")

    def check_input_path(self) -> None:
        """
        Checks if the input path is valid.
        If the input path is not valid, it logs an error message and raises a FileNotFoundError.

        Raises:
            FileNotFoundError: If the input path is not valid.
        """
        # Check if the input path is a file
        if not os.path.isfile(self.input_path):
            # If the input path is not a file, log and raise an error message
            logging.error(f"Invalid input path: {self.input_path}")
            raise FileNotFoundError(f"No file found at specified input path: {self.input_path}")

        logging.info(f"Valid input path: {self.input_path}")

    def check_output_dir(self) -> None:
        """
        Checks if the output directory exists.
        If the output directory does not exist, it logs an error message and raises a FileNotFoundError.

        Raises:
            FileNotFoundError: If the output directory does not exist.
        """
        # Extract the directory name from the output directory path
        output_dir = os.path.dirname(self.output_dir)

        # Check if the directory exists
        if not os.path.isdir(output_dir):
            # If the directory does not exist, log an error and raise an exception
            logging.error(f"Invalid output directory: {output_dir}")
            raise FileNotFoundError(f"The directory for the output path does not exist: {output_dir}")

        logging.info(f"Valid output directory: {output_dir}")

    def produce_preview(self, nodata_value: int = -9999) -> None:
        """
        Generates a preview image from the processed data stored in self.processed_data.
        This method avoids re-reading the data from file, making it more efficient.
        Uses pseudo-color to represent the data visually, ensuring nodata values are transparent.

        Args:
            nodata_value (int, optional): The value representing 'no data' in the dataset. Defaults to -9999.

        Raises:
            ValueError: If the processed data is not available for preview or all data are nodata.
            RuntimeError: If there is an error during the preview generation process.
        """
        try:
            # Check if processed data is available
            if self.processed_data is None:
                logging.error("No processed data available for preview.")
                raise ValueError("Processed data is not available for preview.")

            # Assuming nodata values are set correctly in the processor
            logging.debug(f"Using nodata value: {nodata_value}")

            # Create a mask for valid (non-nodata) values
            valid_mask = self.processed_data != nodata_value
            # Mask the nodata values in the data
            masked_data = np.ma.masked_equal(self.processed_data, nodata_value)
            # If all data are nodata, raise an error
            if masked_data.count() == 0:
                logging.error("All data are nodata. Cannot generate a preview.")
                raise ValueError("All data are nodata. Cannot generate a preview.")

            # Normalize the data to the range [0, 1] for colormap
            normalized_data = (masked_data - masked_data.min()) / (masked_data.max() - masked_data.min())

            # Create an RGBA image where nodata values are set to be transparent
            rgba_image = np.zeros((self.processed_data.shape[0], self.processed_data.shape[1], 4), dtype=np.uint8)
            # Apply colormap to the normalized data
            color_mapped = plt.cm.viridis(normalized_data)
            # Set RGB channels of the image based on the colormap
            rgba_image[..., :3] = (color_mapped[..., :3] * 255).astype(np.uint8)
            # Set alpha channel to transparent if nodata
            rgba_image[..., 3] = (valid_mask * 255).astype(np.uint8)

            # Convert the RGBA image array to a PIL Image object
            self.preview = Image.fromarray(rgba_image, 'RGBA')
            logging.info("Preview generated successfully.")
        except Exception as e:
            logging.error(f"Failed to produce preview: {str(e)}")
            self.preview = None
            # Raise a new error, preserving the original traceback
            raise RuntimeError("Failed to produce preview due to an error.") from e

    def save_processed_data(self, output_path: str, nodata: int = -9999, dtype: str = 'float32') -> None:
        """
        Saves the processed data to a GeoTIFF file using the stored profile.

        Args:
            output_path (str): The path where the processed data will be saved.
            nodata (int, optional): The value representing 'no data' in the dataset. Defaults to -9999.
            dtype (str, optional): The data type of the output GeoTIFF file. Defaults to 'float32'.

        Raises:
            ValueError: If the processed data or the profile is not available for saving.
        """
        # Check if processed data and profile are available
        if self.processed_data is None or self.processor.profile is None:
            logging.error("Processed data or profile is not available for saving.")
            raise ValueError("Processed data or profile is missing.")

        # Update the profile with the provided data type and nodata value
        self.processor.profile.update(dtype=dtype, nodata=nodata)

        # Open the output path as a new GeoTIFF file in write mode
        with rasterio.open(output_path, 'w', **self.processor.profile) as dst:
            # Write the processed data to the first band of the GeoTIFF file
            dst.write(self.processed_data, 1)

        logging.info(f"Processed data saved to {output_path}")

    def create_output_filename(self) -> str:
        """
        Generates a filename based on the input file, current date, and processing parameters.

        The filename is generated in the following format: YYYYMMDD_basename_Surface-Roughness_windowSize-meter.tif

        Returns:
            str: The generated filename with the full path.
        """
        # Extract the base name from the input path (excluding the extension)
        base_name = os.path.splitext(os.path.basename(self.input_path))[0]

        # Get the current date in the format YYYYMMDD
        current_date = datetime.datetime.now().strftime("%Y%m%d")

        # Construct the new filename using the current date, base name, and window size
        new_filename = f"{current_date}_{base_name}_Surface-Roughness_{self.window_size}-meter.tif"

        # Join the output directory path with the new filename to get the full path
        full_path = os.path.join(self.output_dir, new_filename)

        return full_path

    def get_preview(self) -> Image:
        """
        Retrieves the generated preview if available.

        This method checks if a preview image has been generated and is available.
        If the preview is available, it is returned. If not, an error message is logged and a RuntimeError is raised.

        Returns:
            Image: The generated preview image.

        Raises:
            RuntimeError: If the preview is not available or failed to generate.
        """
        # Check if the preview is available
        if self.preview is not None:
            # If the preview is available, return it
            return self.preview
        else:
            # If the preview is not available, log an error message and raise an exception
            error_message = "Preview is not available or failed to generate."
            logging.error(error_message)
            raise RuntimeError(error_message)

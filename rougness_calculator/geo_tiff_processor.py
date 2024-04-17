import logging
import numpy as np
from tif_handler import TifHandler
from roughness_calculator import RoughnessCalculator

logger = logging.getLogger(__name__)


class GeoTIFFProcessor:
    def __init__(self, input_path, output_path):
        """
        Initializes the processor with paths to the input and output TIFF files.

        Args:
            input_path (str): The file path to the input GeoTIFF.
            output_path (str): The file path to the output GeoTIFF where processed data will be saved.
        """
        logger.debug(f"Initializing GeoTIFFProcessor with input: {input_path} and output: {output_path}")
        self.input_path = input_path
        self.output_path = output_path
        self.tif_handler = TifHandler(input_path)
        self.calculator = RoughnessCalculator()

    def process_tiff(self):
        """
        Processes the TIFF file to calculate roughness and save the processed data to an output file.
        Ensures that all resources are properly managed and logs the processing steps.
        """
        try:
            self.load_and_process_data()
        finally:
            self.tif_handler.close()
            logger.info("Processing completed and file closed")

    def load_and_process_data(self):
        """
        Loads the TIFF data, calculates roughness, and saves the result.
        """
        self.tif_handler.load_tiff()
        data = self.tif_handler.read_band()
        pixel_width, pixel_height = self.tif_handler.get_pixel_size()

        logger.info("Calculating roughness")
        roughness = self.calculator.calculate_roughness(data, pixel_width, pixel_height)
        self.apply_nodata_and_save(roughness)

    def apply_nodata_and_save(self, roughness):
        """
        Applies a nodata value to the roughness calculation results and saves the output TIFF.

        Args:
            roughness (np.array): The array containing calculated roughness values.
        """
        nodata_value = -9999  # Define the nodata value that is appropriate for your dataset
        roughness[np.logical_or(roughness == 0, roughness > 1)] = nodata_value
        self.tif_handler.save_tiff(roughness, self.output_path, nodata=nodata_value)

# TODO: Add docstrings and comments

import logging
import numpy as np
import rasterio

logger = logging.getLogger(__name__)


class GeoTIFFProcessor:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.dataset = None

    def load_tiff(self):
        if not self.is_valid_tiff(self.input_path):
            return
        self.dataset = rasterio.open(self.input_path, mode='r')
        logger.info("TIFF file loaded successfully.")

    @classmethod
    def is_valid_tiff(cls, filepath):
        if not filepath or not cls.is_tiff_file(filepath):
            logger.error(f"Invalid or no file selected for the path: {filepath}")
            return False
        logger.info(f"Valid TIFF file confirmed: {filepath}")
        return True

    @staticmethod
    def is_tiff_file(filepath):
        try:
            with open(filepath, 'rb') as file:
                magic_number = file.read(4)
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
        try:
            with rasterio.open(self.input_path) as src:
                logger.info(f"GeoTIFF metadata: {src.meta}")
        except rasterio.errors.RasterioIOError as e:
            logger.error(f"Failed to open GeoTIFF: {e}")
            raise ValueError(f"Invalid GeoTIFF file: {self.input_path}")

    def process_tiff(self):
        self.load_tiff()
        if self.dataset:
            try:
                self.log_tiff_metadata()
                data = self.read_band()
                roughness = self.calculate_roughness(data)
                roughness = self.apply_nodata_and_filter(roughness)
                self.save_tiff(roughness)
            finally:
                self.dataset.close()
                logger.info("Processing completed and file closed")
        else:
            logger.error("Processing aborted due to failed file load.")

    def read_band(self, band_number=1):
        return self.dataset.read(band_number)

    def calculate_roughness(self, data):
        pixel_width, pixel_height = self.get_pixel_size()
        pixels_per_meter_x = int(round(1 / pixel_width))
        pixels_per_meter_y = int(round(1 / pixel_height))
        new_height = data.shape[0] // pixels_per_meter_y
        new_width = data.shape[1] // pixels_per_meter_x
        roughness = np.empty((new_height, new_width))
        for i in range(new_height):
            for j in range(new_width):
                window = data[i*pixels_per_meter_y:(i+1)*pixels_per_meter_y,
                              j*pixels_per_meter_x:(j+1)*pixels_per_meter_x]
                roughness[i, j] = np.std(window)
        return roughness

    @staticmethod
    def apply_nodata_and_filter(roughness, nodata_value=-9999, high_value_threshold=1):
        roughness[np.logical_or(roughness == 0, roughness > high_value_threshold)] = nodata_value
        return roughness

    def save_tiff(self, data, nodata=-9999, dtype='float32'):
        profile = self.dataset.profile
        profile.update(dtype=dtype, nodata=nodata)
        with rasterio.open(self.output_path, 'w', **profile) as dst:
            dst.write(data, 1)
        logger.info("Processed TIFF file saved.")

    def get_pixel_size(self):
        transform = self.dataset.transform
        return transform[0], abs(transform[4])

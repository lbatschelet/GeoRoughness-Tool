import logging
from tif_handler import TifHandler
from roughness_calculator import RoughnessCalculator


logger = logging.getLogger(__name__)

class GeoTIFFProcessor:
    def __init__(self, input_path, output_path):
        logger.debug(f"Initializing GeoTIFFProcessor with input: {input_path} and output: {output_path}")
        self.input_path = input_path
        self.output_path = output_path
        self.tif_handler = TifHandler(input_path)
        self.calculator = RoughnessCalculator()

    def process_tiff(self):
        try:
            self.tif_handler.load_tiff()
            data = self.tif_handler.read_band()
            pixel_width, pixel_height = self.tif_handler.get_pixel_size()

            logger.info("Calculating roughness")
            roughness = self.calculator.calculate_roughness(data, pixel_width, pixel_height)
            nodata_value = -9999
            roughness[roughness == 0] = nodata_value

            self.tif_handler.save_tiff(roughness, self.output_path, nodata=nodata_value)
        finally:
            self.tif_handler.close()
            logger.info("Processing completed and file closed")

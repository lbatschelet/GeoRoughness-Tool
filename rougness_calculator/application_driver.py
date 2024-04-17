# TODO: Add docstrings and comments

import logging
from geo_tiff_processor import GeoTIFFProcessor


class ApplicationDriver:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.setup_logging()
        self.processor = GeoTIFFProcessor(input_path, output_path)

    @staticmethod
    def setup_logging():
        """Sets up the logging configuration."""
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                            filename='app.log',
                            filemode='w')
        logging.info("Logging is configured.")

    def run(self):
        """Runs the processing tasks using the GeoTIFFProcessor."""
        self.processor.process_tiff()
        logging.info("Processing completed.")


def main():
    driver = ApplicationDriver('path/to/your/input.tif', 'path/to/your/output.tif')
    driver.run()


if __name__ == '__main__':
    main()

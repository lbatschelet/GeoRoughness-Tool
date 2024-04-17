import rasterio
import logging
from geo_tiff_processor import GeoTIFFProcessor


def main():
    setup_logging()

    input_path = '/Users/lukasbatschelet/Library/CloudStorage/OneDrive-UniversitaetBern/Studium/FS24/Geoprocessing-II/Projektarbeit_Fotogrammetrie/20240415_Grundlagen/202311xx_Rohdaten/20231116_DEM_Sammler_Obermad_0.05m.tif'
    output_path = '/Users/lukasbatschelet/Library/CloudStorage/OneDrive-UniversitaetBern/Studium/FS24/Geoprocessing-II/Projektarbeit_Fotogrammetrie/05_Output/20231116_DEM_Sammler_Obermad_0.05m.tif'

    if not is_valid_tiff(input_path) or not is_valid_tiff(output_path):
        return

    GeoTIFFProcessor(input_path, output_path)


def setup_logging():
    """Sets up the logging configuration."""
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        filename='app.log',
                        filemode='w')


def is_valid_tiff(filepath):
    """Checks and logs if the given file path is a valid TIFF file."""
    if not filepath or not is_tiff_file(filepath):
        logging.error(f"Invalid or no file selected for the path: {filepath}")
        return False
    logging.info(f"Valid TIFF file confirmed: {filepath}")
    return True


def is_tiff_file(filepath):
    """
    Checks if the given file is a valid TIFF file both by its magic number and by attempting to open it with rasterio.

    Args:
        filepath (str): The path to the file that needs to be validated as a TIFF.

    Returns:
        bool: True if the file is a valid TIFF file, False otherwise.

    Raises:
        IOError: An error occurred accessing the bigfile.
        rasterio.errors.RasterioIOError: An error occurred when trying to open the file with rasterio,
        indicating it may not be a valid TIFF or is unreadable.

    This function first checks the file's magic number to quickly determine if it matches common TIFF signatures.
    If the magic number check passes, it attempts to open the file using rasterio to further validate its structure.
    If either check fails, it logs the appropriate error and returns False.
    """
    try:
        # Check for TIFF magic numbers
        with open(filepath, 'rb') as file:
            magic_number = file.read(4)
        if magic_number not in (b'II\x2A\x00', b'MM\x00\x2A'):
            logging.info("File does not have a valid TIFF magic number.")
            return False

        # Try opening the file with rasterio to further verify it's a valid TIFF
        with rasterio.open(filepath) as src:
            logging.info(f"TIFF file opened successfully with rasterio: {src.meta}")
        return True
    except (IOError, rasterio.errors.RasterioIOError) as e:
        logging.error(f"Failed to open or process TIFF file: {e}")
        return False


def log_tiff_metadata(filepath):
    try:
        with rasterio.open(filepath) as src:
            logging.info(f"GeoTIFF metadata: {src.meta}")
    except rasterio.errors.RasterioIOError as e:
        logging.error(f"Failed to open GeoTIFF: {e}")
        raise ValueError(f"Invalid GeoTIFF file: {filepath}")


if __name__ == '__main__':
    main()

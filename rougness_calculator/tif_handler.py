import rasterio
from roughness_calculator import RoughnessCalculator

class TifHandler:
    def __init__(self, filepath):
        self.filepath = filepath
        self.dataset = None

    def load_tiff(self):
        self.dataset = rasterio.open(self.filepath, mode='r')

    def save_tiff(self, data, output_path, nodata=None, dtype='float32'):
        """
        Speichert ein TIFF mit der Möglichkeit, nodata-Werte zu definieren.

        :param data: Die Datenmatrix, die gespeichert werden soll
        :param output_path: Pfad zur Ausgabedatei
        :param nodata: Der Wert, der als nodata definiert werden soll
        :param dtype: Datentyp der Ausgabe, Standard ist 'float32'
        """
        profile = self.dataset.profile
        profile.update(dtype=dtype, nodata=nodata)
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(data, 1)

    def get_pixel_size(self):
        """
        Returns the pixel dimensions (width, height) from the dataset's transform.
        """
        # Direkter Zugriff auf das Dataset ohne erneutes Öffnen
        if not self.dataset:
            raise RuntimeError("Dataset is not loaded. Please load a dataset first.")

        transform = self.dataset.transform
        pixel_width = transform[0]  # Pixel width in georeferenced units
        pixel_height = abs(transform[4])  # Pixel height in georeferenced units (abs to ensure positive)
        return (pixel_width, pixel_height)

    def read_band(self, band_number=1):
        return self.dataset.read(band_number)

    def close(self):
        self.dataset.close()

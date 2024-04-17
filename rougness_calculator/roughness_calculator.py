import numpy as np
from scipy.ndimage import generic_filter

class RoughnessCalculator:
    def calculate_roughness(self, data, pixel_width, pixel_height):
        """
        Berechnet die Oberflächenrauheit für jedes Pixel im Raster.
        Die Rauheit wird als Standardabweichung der Höhenwerte in einem Fenster um jedes Pixel berechnet.

        :param data: Numpy Array der Rasterdaten (Höhenwerte)
        :param pixel_width: Die Breite eines Pixels in Metern
        :param pixel_height: Die Höhe eines Pixels in Metern
        :return: Ein Numpy Array mit den Rauheitswerten
        """
        # Berechne die Fenstergröße basierend auf der realen Pixelgröße, approximiert auf nahegelegene ganze Zahlen
        window_size_x = max(1, round(1 / pixel_width))  # Stellen Sie sicher, dass das Fenster mindestens 1 Pixel breit ist
        window_size_y = max(1, round(1 / pixel_height)) # Stellen Sie sicher, dass das Fenster mindestens 1 Pixel hoch ist

        def std_deviation(arr):
            return np.std(arr)

        # Erstelle das Rauheitsraster
        roughness = generic_filter(data, std_deviation, size=(window_size_y, window_size_x), mode='nearest')
        return roughness

import numpy as np


class RoughnessCalculator:
    @staticmethod
    def calculate_roughness(data, pixel_width, pixel_height):
        """
        Berechnet die Oberflächenrauheit für jedes 1m x 1m Quadrat im Raster.
        Die Rauheit wird als Standardabweichung der Höhenwerte innerhalb jedes Quadrats berechnet.

        :param data: Numpy Array der Rasterdaten (Höhenwerte)
        :param pixel_width: Die Breite eines Pixels in Metern
        :param pixel_height: Die Höhe eines Pixels in Metern
        :return: Ein Numpy Array mit den Rauheitswerten für jedes 1m x 1m Quadrat
        """
        # Berechne, wie viele Pixel in einem 1m x 1m Quadrat enthalten sind
        pixels_per_meter_x = int(round(1 / pixel_width))
        pixels_per_meter_y = int(round(1 / pixel_height))

        # Größe des Ausgabe-Rasters bestimmen
        new_height = data.shape[0] // pixels_per_meter_y
        new_width = data.shape[1] // pixels_per_meter_x

        # Ausgabe-Array für Rauheitswerte vorbereiten
        roughness = np.empty((new_height, new_width))

        # Jedes Quadrat abgehen und die Standardabweichung berechnen
        for i in range(new_height):
            for j in range(new_width):
                # Start und Ende des aktuellen Quadrats
                start_x = j * pixels_per_meter_x
                start_y = i * pixels_per_meter_y
                end_x = start_x + pixels_per_meter_x
                end_y = start_y + pixels_per_meter_y

                # Extrahiere das Quadrat und berechne die Standardabweichung
                window = data[start_y:end_y, start_x:end_x]
                roughness[i, j] = np.std(window)

        return roughness

import rasterio
import logging

# Konfiguriere das Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def load_geotiff(file_path):
    try:
        logging.info("Lade GeoTIFF-Datei: %s", file_path)
        with rasterio.open(file_path) as dataset:
            # Logge Basisinformationen
            logging.info("Datei erfolgreich geladen.")
            logging.info("CRS: %s", dataset.crs)
            logging.info("Anzahl der Bänder: %d", dataset.count)
            logging.info("Tags (Metadaten) des ersten Bandes: %s", dataset.tags(1))

            # Hier kannst du weitere Aktionen mit dem dataset durchführen

    except Exception as e:
        logging.error("Ein Fehler ist aufgetreten: %s", e)


# Pfad zur GeoTIFF-Datei
file_path = '/Users/lukasbatschelet/Library/CloudStorage/OneDrive-UniversitaetBern/Studium/FS24/Geoprocessing-II/Projektarbeit_Fotogrammetrie/20240415_Grundlagen/202311xx_Rohdaten/20231116_DEM_Sammler_Obermad_0.05m.tif'

# Funktion aufrufen
load_geotiff(file_path)

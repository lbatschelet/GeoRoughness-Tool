import logging
from geo_tiff_processor import GeoTIFFProcessor



def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                        filename='app.log',
                        filemode='w')

    input_path = '/Users/lukasbatschelet/Library/CloudStorage/OneDrive-UniversitaetBern/Studium/FS24/Geoprocessing-II/Projektarbeit_Fotogrammetrie/20240415_Grundlagen/202311xx_Rohdaten/20231116_DEM_Sammler_Obermad_0.05m.tif'
    output_path = '/Users/lukasbatschelet/Library/CloudStorage/OneDrive-UniversitaetBern/Studium/FS24/Geoprocessing-II/Projektarbeit_Fotogrammetrie/05_Output/20231116_DEM_Sammler_Obermad_0.05m.tif'

    if not input_path:
        logging.error("Keine Eingabedatei ausgewählt.")
        return
    logging.info(f"Verarbeite GeoTIFF: {input_path}")
    if not output_path:
        logging.error("Keine Ausgabedatei festgelegt.")
        return
    logging.info(f"Ausgabe GeoTIFF: {output_path}")

    logging.info(f"Anwendungsstart - Eingabedatei: {input_path}, Ausgabedatei: {output_path}")

    try:
        processor = GeoTIFFProcessor(input_path, output_path)
        processor.process_tiff()
        logging.info("Verarbeitung erfolgreich abgeschlossen.")
    except Exception as e:
        logging.error(f"Ein Fehler ist aufgetreten: {str(e)}")
        raise

if __name__ == '__main__':
    main()

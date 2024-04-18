"""
cli_main.py
-----------
Version: 0.1.0
Author: Lukas Batschelet
Date: 18.04.2024
-----------
FOR TESTING PURPOSES ONLY

This module acts as the testing entry point for the application.
It is responsible for running the application in a command-line interface (CLI) environment.
It initializes the ApplicationDriver with the input and output paths and runs the application.
The final version of the application is intended to be run using the GUI provided in gui_main.py.
"""
from application_driver import ApplicationDriver


def main():
    """
    Main function for running the application in a CLI environment.
    The input and output paths are hardcoded in this script for testing purposes.
    """

    input_path = '/Users/lukasbatschelet/Library/CloudStorage/OneDrive-UniversitaetBern/Studium/FS24/Geoprocessing-II/Projektarbeit_Fotogrammetrie/20240415_Grundlagen/202311xx_Rohdaten/20231116_DEM_Sammler_Obermad_0.05m.tif'
    output_dir = '/Users/lukasbatschelet/Library/CloudStorage/OneDrive-UniversitaetBern/Studium/FS24/Geoprocessing-II/Projektarbeit_Fotogrammetrie/05_Output'
    window_size = 2

    driver = ApplicationDriver(input_path, output_dir, window_size)
    driver.run()


# Run the application in a CLI environment
if __name__ == '__main__':
    main()

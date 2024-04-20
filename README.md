# DEM Roughness Calculator

This is a Python script that calculates the roughness of a Digital Elevation Model (DEM) using
the standard deviation of the height information in a window of a given size.

> [!important]
> This module is still in development, especially the user interface and general documentation are lacking.
> If you have any questions or suggestions, feel free to contact me.
> Errors and bugs can be reported in the issues section of the repository.


## Current state

- [ ] [`geo_tiff_processor.py`](./roughness_calculator/geo_tiff_processor.py) - Module for processing GeoTIFF files
  - [X] Load GeoTIFF file
  - [X] Read GeoTIFF file metadata
  - [X] Calculate roughness of GeoTIFF file using a given window size by calculating the standard deviation of the height
        information in the window
  - [X] Save GeoTIFF file
  - [X] Generate pseudocolored preview of GeoTIFF file for GUI
  - [X] Added following functionality:
    - [X] Accept `window_size` in meters as parameter.
    - [X] Accept `band_number` as parameter.
    - [X] Accept `high_value_threshold` as parameter.
    - [X] Accept `category_thresholds` as parameter.
  - [ ] Add functionality to only save the file when wanted after seeing the preview.
  - [ ] Add tests
  - [ ] Add documentation
  - [ ] Add clearer logging
  - [ ] Add error handling
  - [ ] Add type hints
- [ ] [`application_driver.py`](./roughness_calculator/application_driver.py) - Module for running the application
  - [X] Implement interface to run the application both as a CLI and a GUI
  - [ ] Implement functionality to handover the generated GeoTIFF file to the GUI
  - [ ] Add tests
  - [ ] Add documentation
  - [ ] Add clearer logging
  - [ ] Add error handling
  - [ ] Add type hints
- [ ] [`dem_roughness_calculator.py`](./roughness_calculator/dem_roughness_calculator.py) - GUI programm
  - [X] Create GUI to run the programm
  - [X] Add functionality to load a GeoTIFF file
  - [X] Add functionality to set the window size for the roughness calculation
  - [X] Add functionality to set the band number of the GeoTIFF file
  - [X] Add functionality to set the high value threshold for the roughness calculation
  - [X] Add functionality to calculate the roughness of the GeoTIFF file
  - [X] Add functionality to save the result as a new GeoTIFF file
  - [ ] implement funcionality to only save the file when wanted after seeing the preview.
  - [ ] Add tests
  - [ ] Add documentation
  - [ ] Add clearer logging
  - [ ] Add error handling
  - [ ] Add type hints


## How to get going

For a detailed quide on how to get started with the project, see the
[Getting Started wiki page](https://github.com/lbatschelet/dem-roughness-calculator/wiki/How-to-get-going) guide.
This guide will walk you through the steps needed to set up the project and run the GUI version of the application.

For a detailed guide on how to use the CLI version of the application, see the
[CLI Usage wiki page](https://github.com/lbatschelet/dem-roughness-calculator/wiki/GeoTIFF-Surface-Roughness-Calculator-CLI)


## Functionality

The program allows you to calculate the surface roughness of a Digital Elevation Model (DEM).
You can load a DEM file in the GeoTIFF format and set the window size for the calculation. It then calculates
the roughness of the DEM by computing the standard deviation of the height information in the window of the given size.
The result is output in a new GeoTIFF file.

## How to use the program

1. Select the DEM file you want to calculate the roughness with.
2. Select an output directory where the result will be saved.
3. Set the side length of the square window size in meters for the calculation.
   If left empty it will default to 1 meter.
4. Set the band number of the DEM file.
   If left empty it will default to 1.
5. Set the high value threshold for the roughness calculation. This value is used to filter out abnormally high 
   roughness values that are likely to be errors that would skew the results. 
   If left empty it will default to 1. Should not need to be changed in most cases.


## Needed libraries

The script uses the following libraries:

- [Affine (2.4.0):](https://pypi.org/project/affine/) Matrices describing affine transformation of the plane
- [Attrs (23.2.0):](https://www.attrs.org/en/stable/) Classes Without Boilerplate
- [Certifi (2024.2.2):](https://pypi.org/project/certifi/) Python package for providing Mozilla's CA Bundle.
- [Click (8.1.7):](https://click.palletsprojects.com/en/8.0.x/) Composable command line interface toolkit
- [Click-Plugins (1.1.1):](https://pypi.org/project/click-plugins/) An extension module for click to enable registering
  CLI commands via setuptools entry-points.
- [Cligj (0.7.2):](https://pypi.org/project/cligj/) Click params for common GIS formats
- [NumPy (1.26.4):](https://numpy.org/) The fundamental package for scientific computing with Python
- [Pyparsing (3.1.2):](https://pypi.org/project/pyparsing/) Python parsing module
- [Rasterio (1.3.10):](https://rasterio.readthedocs.io/en/latest/) access to geospatial raster data
- [SciPy (1.13.0):](https://www.scipy.org/) Fundamental algorithms for scientific computing in Python
- [Setuptools (69.5.1):](https://pypi.org/project/setuptools/) Easily download, build, install, upgrade, and 
  uninstall Python packages
- [Snuggs (1.4.7):](https://pypi.org/project/snuggs/) Snuggs are s-expressions for numpy
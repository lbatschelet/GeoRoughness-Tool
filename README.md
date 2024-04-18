# DEM Roughness Calculator

This is a Python script that calculates the roughness of a Digital Elevation Model (DEM) using
the standard deviation of the height information in a window of a given size.

## How to get going

1. Install `python 3.8` or higher.
   You can download it from the [official website](https://www.python.org/downloads/).
2. Check that `pip` is installed. It is a package installer for Python that is usually installed as part of the Python 
   installation. You can check it by running the following command in your terminal
   ```bash
   pip --version
   ```
   If it is not installed, you can install it by following the instructions on the 
   [official website](https://pip.pypa.io/en/stable/installation/).
3. Check that `git` is installed. It is a version control system.
   You can check it by running the following command in your terminal
   ```bash
   git --version
   ```
   If it is not installed, you can install it by following the instructions on the 
   [official website](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).
4. Select a directory where you want to clone the repository.
   You can do that by running the following command in your terminal:
      ```bash
      cd /path/to/your/directory
      ```
5. Clone the repository to your local machine.
   You can do that by running the following command in your terminal:
   ```bash
   git clone https://github.com/lbatschelet/dem-roughness-calculator.git
   ```
6. Install the required libraries by running the following command in your terminal:
   ```bash
   pip install -r requirements.txt
   ```
7. Run the script by running the following command in your terminal:
   ```bash
   python3 ./roughness_calculator/gui_main.py
   ```
   
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
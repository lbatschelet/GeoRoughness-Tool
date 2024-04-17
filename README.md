# DEM Roughness Calculator

This is a Python script that calculates the roughness of a Digital Elevation Model (DEM) using 
the standard deviation of the slope.

## Needed libraries

- [SciPy:](https://www.scipy.org/) Fundamental algorithms for scientific computing in Python
- [NumPy:](https://numpy.org/) The fundamental package for scientific computing with Python
- [Rasterio:](https://rasterio.readthedocs.io/en/latest/) access to geospatial raster data

These libraries need to be installed in your Python environment before running the script.
To install the libraries, you can use the following command in your terminal:
```bash
pip install numpy scipy rasterio
```

## Usage

The simplest way to use the script is to run the GUI version.
In the GUI version, you can select the DEM file and the output file. The output file should also be a `.tif` file.
```bash
python3 ./roughness_calculator/main_gui.py
```
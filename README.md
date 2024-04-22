# DEM Roughness Calculator

The DEM Roughness Calculator is a comprehensive tool designed for geospatial analysis, allowing users to calculate the surface roughness of Digital Elevation Models (DEMs) using the standard deviation of height within a specified window size. The tool is equipped with both a graphical user interface (GUI) and a command-line interface (CLI), making it versatile for different user preferences and workflows.

## Features

- **GeoTIFF Support**: Load and process DEM data directly from GeoTIFF files.
- **Flexible Window Sizes**: Specify the window size in meters for roughness calculations.
- **Advanced Thresholding**: Configure high value and categorical thresholds to refine processing.
- **Dual Interface**: Operate through a user-friendly GUI or a powerful CLI.
- **Dynamic Previews**: Generate and view pseudo-colored previews of the processed DEM within the GUI.
- **Selective Saving**: Choose when to save processed outputs after reviewing results.

## Installation Guide for DEM Roughness Calculator

This guide provides detailed steps for installing the DEM Roughness Calculator on Windows, macOS, and Linux systems. Please follow the instructions specific to your operating system.

### Prerequisites

Before you begin, ensure that your system meets the following requirements:
- **Python 3.12 or later**: The software is built to run with Python 3.12 and above.
- **pip**: Python's package installer, used to install the DEM Roughness Calculator.

### Step-by-Step Installation

<details>
<summary>Windows</summary>

#### Windows

1. **Install Python**:
   - Visit the [official Python website](https://www.python.org/downloads/).
   - Download the installer for Python 3.12 or later.
   - Run the installer. Ensure to check the box that says "Add Python 3.12 to PATH" at the beginning of the installation process.
   - Complete the installation.

2. **Verify Installation**:
   - Open Command Prompt and type:
     ```
     python --version
     ```
     This should display the Python version installed.
   - Check pip is installed:
     ```
     pip --version
     ```

3. **Install DEM Roughness Calculator**:
   - In the Command Prompt, run:
     ```
     pip install dem-roughness-calculator
     ```
</details>

<details>
<summary>macOS</summary>

#### macOS

1. **Install Python**:
   - You can install Python using Homebrew (a package manager for macOS). If you do not have Homebrew installed, you can install it by pasting the following command in a Terminal window:
     ```
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
   - Once Homebrew is installed, install Python by running:
     ```
     brew install python@3.12
     ```

2. **Verify Installation**:
   - In the Terminal, run:
     ```
     python3 --version
     ```
     - This should return the version of Python installed.
   - Ensure pip is working:
     ```
     pip3 --version
     ```

3. **Install DEM Roughness Calculator**:
   - In the Terminal, run:
     ```
     pip3 install dem-roughness-calculator
     ```
</details>

<details>
<summary>Linux</summary>

#### Linux

1. **Install Python**:
   - Most Linux distributions come with Python pre-installed. If not, you can install it using your distribution’s package manager. For Ubuntu, use:
     ```
     sudo apt update
     sudo apt install python3.12 python3-pip
     ```

2. **Verify Installation**:
   - Check Python installation:
     ```
     python3 --version
     ```
   - Check pip installation:
     ```
     pip3 --version
     ```

3. **Install DEM Roughness Calculator**:
   - Use pip to install:
     ```
     pip3 install dem-roughness-calculator
     ```
</details>

## Usage

### GUI Application

To launch the GUI, simply run the following command in your terminal:

```bash
demgui
```

The graphical interface allows you to browse for input files, set processing parameters, and view the roughness map interactively before deciding to save the output.

### CLI Application

For those who prefer working in a command-line environment, the CLI provides a robust solution. Here’s how to use it:

```bash
demcli --input_path "path/to/input.tif" --output_dir "path/to/output" --window_size 1.0 --band_number 1 --high_value_threshold 1.0 --categorical_thresholds 0.1 0.2 0.3
```

### Parameters

- **`--input_path`**: Path to the input GeoTIFF file.
- **`--output_dir`**: Directory where the output files will be saved.
- **`--window_size`** (optional): The size of the window in meters for calculating roughness.
- **`--band_number`** (optional): The specific band of the DEM to process.
- **`--high_value_threshold`** (optional): Threshold to filter out high elevation values.
- **`--categorical_thresholds`** (optional): Set of thresholds to categorize the elevation data.

## Documentation

For more detailed information about the tool's capabilities and additional configurations, please refer to the [Wiki](https://github.com/lbatschelet/dem-roughness-calculator/wiki).

## Contributing

We welcome contributions! If you have suggestions or want to report bugs, please use the [Issues](https://github.com/lbatschelet/dem-roughness-calculator/issues) section of this repository.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.
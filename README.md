# DEM Roughness Calculator

The DEM Roughness Calculator is a comprehensive tool designed for geospatial analysis, allowing users to calculate the surface roughness of Digital Elevation Models (DEMs) using the standard deviation of height within a specified window size. The tool is equipped with both a graphical user interface (GUI) and a command-line interface (CLI), making it versatile for different user preferences and workflows.

## Features

- **GeoTIFF Support**: Load and process DEM data directly from GeoTIFF files.
- **Flexible Window Sizes**: Specify the window size in meters for roughness calculations.
- **Advanced Thresholding**: Configure high value and categorical thresholds to refine processing.
- **Dual Interface**: Operate through a user-friendly GUI or a powerful CLI.
- **Dynamic Previews**: Generate and view pseudo-colored previews of the processed DEM within the GUI.
- **Selective Saving**: Choose when to save processed outputs after reviewing results.

## Documentation

For more detailed information about the tool's capabilities and additional configurations, 
please refer to the [Project's Wiki](https://github.com/lbatschelet/dem-roughness-calculator/wiki).

## Installation Guide for DEM Roughness Calculator

Follow these steps to install the DEM Roughness Calculator on your system. The program is available
as a Python package and can therefore be installed on any major operating system.

> [!TIP]
> If you are not that experienced using command line tools or experience any problems during installation, please refer to the [Getting Started Wiki Page](https://github.com/lbatschelet/dem-roughness-calculator/wiki/Getting-Started) for a more detailed and OS specific installation guide.

### Prerequisites

Before you begin, ensure that your system meets the following requirements:
- **Python 3.12 or later**: The software is built to run with Python 3.12 and above.
- **pip**: Python's package installer, used to install the DEM Roughness Calculator.

### Step-by-Step Installation

#### 1. Install Python
Ensure you have Python 3.12 or later installed on your computer:
- **Windows**: Download from the [official Python website](https://www.python.org/downloads/). Make sure to add Python to PATH during installation.
- **macOS**: Install using Homebrew with `brew install python@3.12`.
- **Linux**: Use your package manager, e.g., for Ubuntu: `sudo apt install python3.12 python3-pip`.

#### 2. Verify Installation
Check Python and pip installation:
```bash
python3 --version
pip3 --version
```

#### 3. Install DEM Roughness Calculator
Install the package via pip:
```bash
pip3 install dem-roughness-calculator
```

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
demcli --input_path "path/to/input.tif" --output_dir "path/to/output" --window_size 1.0 --band_number 1 --high_value_threshold 1.0 --categorical_thresholds 0.1, 0.2, 0.3
```

### Parameters

- **`--input_path`**: Path to the input GeoTIFF file.
- **`--output_dir`**: Directory where the output files will be saved.
- **`--window_size`** (optional): The size of the window in meters for calculating roughness.
- **`--band_number`** (optional): The specific band of the DEM to process.
- **`--high_value_threshold`** (optional): Threshold to filter out high elevation values.
- **`--categorical_thresholds`** (optional): Set of thresholds to categorize the elevation data.

## Disclaimer

> [!NOTE]
> **AI-Assisted Development**
> 
> This project leverages artificial intelligence, including OpenAI's GPT-4 and GitHub Copilot, to assist in generating parts of the code and documentation. These tools provide suggestions that enhance the development process and help in crafting more robust and comprehensive materials. While AI tools have been instrumental in accelerating development and improving productivity, the final decisions on the inclusion and modification of the generated content rest solely with the human developers. This ensures that each aspect of the project aligns with our quality standards and functional requirements. 
> 
> Please note that while AI has contributed to the project, it may not capture the full complexity or context of the development practices. As such, any anomalies or errors introduced by AI-generated content have been reviewed and rectified to the best of our capabilities. However, users should exercise their judgment and discretion when using or modifying this software. 
> 
> For any concerns or questions about the AI-generated content within this project, please feel free to contact us through the repository's issues section.

## Contributing

We welcome contributions! If you have suggestions or want to report bugs, please use the [Issues](https://github.com/lbatschelet/dem-roughness-calculator/issues) section of this repository.

## License

This project is licensed under the GPL-3.0 License - see the [LICENSE](LICENSE) file for details.

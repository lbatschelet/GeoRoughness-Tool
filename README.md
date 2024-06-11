![GitHub Repo stars](https://img.shields.io/github/stars/lbatschelet/GeoRoughness-Tool)
![PyPI - License](https://img.shields.io/pypi/l/geo-roughness-tool)
![PyPI - Downloads](https://img.shields.io/pypi/dm/geo-roughness-tool)
![PyPI - Version](https://img.shields.io/pypi/v/geo-roughness-tool)

![GeoRoughness_Banner_dark.png](.github%2Fresources%2FGeoRoughness_Banner_dark.png#gh-dark-mode-only)
![GeoRoughness_Banner_light.png](.github%2Fresources%2FGeoRoughness_Banner_light.png#gh-light-mode-only)


# GeoRoughness Tool

This is a spatial analysis tool for calculating surface roughness from Digital Elevation Models (DEMs). The tool 
provides a comprehensive solution for geospatial analysis, allowing users to compute roughness values based on the
standard deviation of height within a specified window size. The tool allows for easy classification of roughness values
and generation of roughness maps for visualizing the terrain's variability.

## Features

- **Surface Roughness Calculation**: Compute roughness values based on the standard deviation of height.
- **Surface Roughness Mapping**: Generate roughness maps for visualizing the terrain's variability.
- **Surface Roughness Classification**: Categorize roughness values into different classes.
- **Classification Quality Metrics**: Evaluate the quality of the classification using accuracy metrics.
- **Classification Optimization**: Optimize the classification thresholds for better results.

---

## Documentation

For more detailed information about the tool's capabilities and additional configurations, 
please refer to the [Project's Wiki](../../wiki).

## Installation Guide for GeoRoughness Tool

Follow these steps to install the GeoRoughness Tool on your system. The program is available
as a Python package and can therefore be installed on any major operating system.

> [!TIP]
> If you are not that experienced using command line tools or experience any problems during installation, please refer 
> to the [Getting Started Wiki Page](../../wiki/Getting-Started) for a more detailed and OS specific installation guide.

### Prerequisites

Before you begin, ensure that your system meets the following requirements:
- **Python 3.12 or later**: The software is built to run with Python 3.12 and above.
- **pip**: Python's package installer, used to install the GeoRoughness Tool.

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

#### 3. Install GeoRoughness Tool
Install the package via pip:
```bash
pip3 install geo-roughness-tool
```

---

## Usage

To launch the Application, simply run the following command in your terminal after installation:

```bash
georough
```

---

### CLI Application

This package also provides a basic command line interface (CLI) for batch processing of DEM files. For more information 
on how to use the CLI, please refer to the [CLI Documentation](../../wiki/Getting-Started#CLI-Application).

---

## AI-Assisted Development

> [!NOTE]
> This project leverages artificial intelligence, including OpenAI's GPT-4, GPT-4o and GitHub Copilot, to assist in generating parts of the code and documentation. These tools provide suggestions that enhance the development process and help in crafting more robust and comprehensive materials. While AI tools have been instrumental in accelerating development and improving productivity, the final decisions on the inclusion and modification of the generated content rest solely with the human developers. This ensures that each aspect of the project aligns with our quality standards and functional requirements. 
> 
> Please note that while AI has contributed to the project, it may not capture the full complexity or context of the development practices. As such, any anomalies or errors introduced by AI-generated content have been reviewed and rectified to the best of our capabilities. However, users should exercise their judgment and discretion when using or modifying this software. 
> 
> For any concerns or questions about the AI-generated content within this project, please feel free to contact us through the repository's issues section.

---

## Contributing

We welcome contributions! If you have suggestions or want to report bugs, please use the [Issues](../../issues) section of this repository.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

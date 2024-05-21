from setuptools import setup, find_packages

# Read the contents of your requirements file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='geo_roughness_tool',
    version='0.0.1',
    packages=find_packages(),  # Automatically find all packages in the directory
    url='https://github.com/lbatschelet/geo-rougness-tool',
    license='GPL-3.0',
    author='lbatschelet',
    description='A package for calculating surface roughness using GeoTIFF DEM files with a GUI and CLI',
    install_requires=requirements,  # Install dependencies from requirements.txt
    python_requires='>=3.12',  # Specify Python version requirement
    entry_points={
        'console_scripts': [
            'geo_roughness_tool=geo_roughness_tool.main:main',
            'demgui=geo_roughness_tool.old_entry_points.demgui:main',
            'demcli=geo_roughness_tool.old_entry_points.demcli:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: GIS'
    ]
)

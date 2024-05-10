from setuptools import setup, find_packages

# Read the contents of your requirements file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='dem-roughness-calculator',
    version='1.2.1',
    packages=find_packages(),  # Automatically find all packages in the directory
    url='https://github.com/lbatschelet/dem-roughness-calculator',
    license='GPL-3.0',
    author='lbatschelet',
    description='A package for calculating surface roughness using GeoTIFF DEM files with a GUI and CLI',
    install_requires=requirements,  # Install dependencies from requirements.txt
    python_requires='>=3.12',  # Specify Python version requirement
    entry_points={
        'console_scripts': [
            'surface-roughness=main:main',
            'demgui=roughness_calculator.old_entry_points.demgui:main',
            'demcli=roughness_calculator.old_entry_points.demcli:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',  # Update as appropriate for your release cycle
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: GIS'
    ]
)

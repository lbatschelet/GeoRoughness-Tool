from setuptools import setup, find_packages

# Read the contents of your requirements file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='georoughness-tool',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url='https://github.com/lbatschelet/GeoRoughness-Tool',
    license='MIT',
    author='lbatschelet',
    description='A package for calculating surface roughness using GeoTIFF DEM files with a GUI and CLI',
    install_requires=requirements,  # Install dependencies from requirements.txt
    python_requires='>=3.12',  # Specify Python version requirement
    entry_points={
        'console_scripts': [
            'georough=geo_roughness_tool.main:main',
            'dingsbums=geo_roughness_tool.main:main',
            'giraffe=geo_roughness_tool.main:main',
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',  # Update as appropriate for your release cycle
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: GIS'
    ]
)

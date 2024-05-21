import os
from setuptools import setup, find_packages

# Read the contents of your README file
def read(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()

# Read the contents of your requirements file
def read_requirements(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

setup(
    name='geo-roughness-tool',
    use_scm_version=True,  # Automatically set the version from Git tags
    setup_requires=['setuptools_scm'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url='https://github.com/lbatschelet/GeoRoughness-Tool',
    license='MIT',
    author='Lukas Batschelet',
    author_email='your-email@example.com',  # Replace with your email
    description='A package for calculating surface roughness using GeoTIFF DEM files with a GUI and CLI',
    long_description=read('README.md'),  # Use the README.md as the long description
    long_description_content_type='text/markdown',
    install_requires=read_requirements('requirements.txt'),  # Install dependencies from requirements.txt
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
    ],
    project_urls={  # Optional
        'Documentation': 'https://github.com/lbatschelet/GeoRoughness-Tool/wiki',
        'Source': 'https://github.com/lbatschelet/GeoRoughness-Tool',
        'Tracker': 'https://github.com/lbatschelet/GeoRoughness-Tool/issues',
    },
    keywords='GIS, GeoTIFF, DEM, surface roughness, geographic information systems',  # Add relevant keywords
)

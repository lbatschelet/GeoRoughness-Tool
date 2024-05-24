import os
from setuptools import setup, find_packages

def read(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()

def read_requirements(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read().splitlines()

def _clean_version():
    """
    Custom version scheme to avoid .dev and .post versions.
    """
    def get_version(version):
        if version.exact:
            return version.format_with("{tag}")
        else:
            return version.format_next_version("{tag}.post{distance}")

    def empty(version):
        return ''

    return {'local_scheme': get_version, 'version_scheme': empty}

setup(
    name='geo-roughness-tool',
    use_scm_version=_clean_version,  # Assign the callable directly
    setup_requires=["setuptools-scm"],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url='https://github.com/lbatschelet/GeoRoughness-Tool',
    license='MIT',
    author='Lukas Batschelet',
    description='A package for calculating surface roughness using GeoTIFF DEM files with a GUI and CLI',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=read_requirements('requirements.txt'),
    python_requires='>=3.12',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'georough=geo_roughness_tool.main:main',
            'dingsbums=geo_roughness_tool.main:main',
            'giraffe=geo_roughness_tool.main:main',
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
    ],
    project_urls={
        'Documentation': 'https://github.com/lbatschelet/GeoRoughness-Tool/wiki',
        'Source': 'https://github.com/lbatschelet/GeoRoughness-Tool',
        'Tracker': 'https://github.com/lbatschelet/GeoRoughness-Tool/issues',
    },
    keywords='GIS, GeoTIFF, DEM, surface roughness, geographic information systems',
)

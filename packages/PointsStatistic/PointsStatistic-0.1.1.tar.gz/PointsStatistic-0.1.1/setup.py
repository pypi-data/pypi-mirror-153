# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
	
# This call to setup() does all the work
setup(
    name="PointsStatistic",
    version="0.1.1",
    description="Library to count POIs around reference points, and distance of the closest ones",
    long_description="This class defines two functions: 1 - Given a points shapefile of reference points, a list of polygon shapefile that subdivide the study area, a radius r of interest, the desired coordinate reference system (crs), and a series of points shapefile containing the point of interests (POIs), counts the numbers of POIs inside the defined radius r from the reference points. This number is added to a new database column 2 - Given a points shapefile of reference points, a list of polygon shapefile that subdived the study area, the desired coordinate reference system (crs), and a series of points shapefile containing the point of interests (POIs), returns the distance between the reference point and the closest POI. The result is added to a new database column",
    long_description_content_type="text/markdown",
    url="https://PointsStatistics.readthedocs.io/",
    author="Francesco Niccolò Polinelli",
    author_email="francescon.polinelli@gmail.com",
    license="Free for non-commercial use",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: Free for non-commercial use",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["PointsStatistics"],
    include_package_data=True,
    install_requires=["os", "time", "pandas", "geopandas", "shapely"]
)
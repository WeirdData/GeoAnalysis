#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#  Data Source: https://data.worldbank.org/indicator/NY.GDP.MKTP.CD

import csv

import cartopy.crs as crs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib
import matplotlib.pyplot as plt
from SecretColors import Palette

matplotlib.rc("font", family="IBM Plex Sans")

p = Palette('brewer')

COL_2019_GDP = 63
COL_COUNTRY_NAME = 0
COL_COUNTRY_CODE = 1


def get_data():
    data = []
    with open("data/gdp.csv") as f:
        for row in csv.reader(f):
            if len(row[COL_2019_GDP]) > 0:
                data.append((row[COL_COUNTRY_NAME],
                             row[COL_COUNTRY_CODE],
                             float(row[COL_2019_GDP]) / 1000000000))

    return data


def draw_map():
    # Generate counts before drawing the map
    data = get_data()
    data = {x[1]: x for x in data if x[2] <= 186}

    plt.figure(figsize=(11, 9))
    ax = plt.subplot(111, projection=crs.Miller())

    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()
    # ax.add_feature(cfeature.OCEAN, color=p.blue(shade=30))
    ax.add_feature(cfeature.BORDERS, alpha=0.5)
    ax.add_feature(cfeature.COASTLINE, alpha=0.5)

    for country in countries:
        ct = country.attributes['ADM0_A3']
        if ct in data.keys():
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=p.red(shade=40),
                              alpha=0.8)
        else:
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=p.gray(shade=20),
                              alpha=0.8)

    plt.title("Economic inequality in the World")
    plt.savefig("plot.png", dpi=300)
    plt.show()


def run():
    draw_map()

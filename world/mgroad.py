#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#  Data: https://en.wikipedia.org/wiki/List_of_roads_named_after_Mahatma_Gandhi
import csv

import cartopy.crs as crs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib
import matplotlib.pyplot as plt
from SecretColors import Palette

matplotlib.rc("font", family="IBM Plex Sans")

p = Palette('brewer')


def get_data():
    mapping = {}
    with open("data/country-codes.csv") as f2:
        for row in csv.reader(f2):
            mapping[row[0]] = row[2]

    data = []
    with open("data/mgroad") as f:
        for line in f:
            data.append(mapping[line.strip()])

    return data


def draw_map():
    # Generate counts before drawing the map
    data = get_data()

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
        if ct in data:
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=p.violet(shade=40),
                              alpha=0.8)
        else:
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=p.gray(shade=20),
                              alpha=0.8)

    plt.title("Countries where at least one road is named after Mahatma "
              "Gandhi")
    plt.annotate("Grey countries either do not have any road named after\n"
                 "Mahatma Gandhi or data is not available",
                 xy=(0.9, 0.12),
                 xycoords="figure fraction",
                 va="top",
                 ha="right")
    plt.savefig("plot.png", dpi=300)
    plt.show()


def run():
    draw_map()

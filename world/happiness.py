#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#  Data: https://www.kaggle.com/unsdsn/world-happiness

import csv
import cartopy.crs as crs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib
import matplotlib.pyplot as plt
from SecretColors import Palette
from matplotlib.patches import Patch

matplotlib.rc("font", family="IBM Plex Sans")

p = Palette('brewer')


def get_codes():
    data = {}
    with open("data/country-codes.csv") as f:
        for row in csv.reader(f):
            data[row[0]] = row[2]
    return data


def get_data():
    codes = get_codes()
    data = {}
    with open("data/happiness_2019.csv")as f:
        next(f)
        for row in csv.reader(f):
            data[row[1]] = float(row[2])

    data = {codes[k]: v for k, v in data.items()}
    return data


def draw_map():
    # Generate counts before drawing the map
    data = get_data()

    plt.figure(figsize=(12, 8))
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
            if data[ct] > data["IND"]:
                color = p.ultramarine(shade=30)
            elif ct == "IND":
                color = p.red(shade=20)
            else:
                color = p.red(shade=40)
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=color,
                              alpha=0.8)
        else:
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=p.gray(shade=20),
                              alpha=0.8)

    handles = [
        Patch(fc=p.red(shade=20), label="India"),
        Patch(fc=p.ultramarine(shade=30), label="Happier than India"),
        Patch(fc=p.red(shade=40), label="Unhappier than India"),
        Patch(fc=p.gray(shade=20), label="No Data"),
    ]
    plt.legend(handles=handles, loc="lower left", framealpha=1)
    plt.title("Countries Happier than India")
    plt.annotate("Based on 2019 World Happiness Report\nIndia ranks at 140 "
                 "out of 156 countries",
                 xy=(0.98, 0.05),
                 xycoords="axes fraction",
                 va="top",
                 ha="right")
    plt.tight_layout()
    plt.savefig("plot.png", dpi=150)
    plt.show()


def run():
    draw_map()

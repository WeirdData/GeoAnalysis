#  WeirdData Copyright (c) 2021.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#  data:
#  https://www.who.int/malaria/areas/elimination/malaria-free-countries/en/

import pandas as pd
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


def get_data() -> pd.DataFrame:
    df = pd.read_csv("data/malaria_certified.csv")
    df = df.set_index("country")
    countries = pd.read_csv("data/country-codes.csv")
    countries = countries.set_index("name")
    df = pd.concat([df, countries], axis=1, join="inner")
    col = "Alpha-3 code"
    df = df[[col, "certified", "never"]]
    df = df.rename_axis("country")
    df = df.reset_index()
    return df


def plot_map():
    data = get_data()
    data = data.rename(columns={"Alpha-3 code": "code"})
    data = data.set_index("country")
    certified = data[["code", "certified"]]
    certified = certified.dropna()
    certified = dict(zip(certified["code"], certified["certified"]))
    never = data[["code", "never"]]
    never = never.dropna()
    never = dict(zip(never["code"], never["never"]))

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
        if ct in certified.keys():
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=p.green(shade=30))
        elif ct in never.keys():
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=p.green(shade=60))
        else:
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=p.gray(shade=20),
                              alpha=0.8)

    handles = [
        Patch(fc=p.green(shade=60), label="Never existed or vanished\n"
                                          "without measure"),
        Patch(fc=p.green(shade=30), label="Certified Malaria Free"),
    ]
    plt.legend(handles=handles, loc="lower left", framealpha=1)
    plt.title("Malaria Free Countries in 2019")
    plt.annotate("Countries that have achieved at least 3 consecutive\n"
                 " years of zero indigenous cases are eligible to apply\n"
                 "for a WHO certification of malaria-free status.",
                 xy=(0.98, 0.02),
                 xycoords="axes fraction",
                 ha="right",
                 fontsize=8,
                 color=p.gray(shade=80),
                 bbox=dict(facecolor=p.white(), ec="None", alpha=0.8),
                 va="bottom")
    plt.tight_layout()
    plt.savefig("plot.png", dpi=300)
    plt.show()


def run():
    plot_map()

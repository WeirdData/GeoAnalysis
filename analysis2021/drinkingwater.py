#  WeirdData Copyright (c) 2021.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#  Data from :
#  https://www.kaggle.com/utkarshxy/who-worldhealth-statistics-2020-complete

import cartopy.crs as crs
import cartopy.feature as cfeature
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from SecretColors import Palette
from SecretColors.cmaps import BrewerMap
from mpl_toolkits.axes_grid1 import make_axes_locatable

from helpers.functions import country_codes, get_shapes


def get_data():
    df = pd.read_csv("data/basicDrinkingWater.csv")
    codes = country_codes(df["Location"].to_list())
    df["Location"] = df["Location"].map(lambda x: codes[x])
    df["First Tooltip"] /= 100
    df = dict(zip(df["Location"], df["First Tooltip"]))
    return df


def draw_map():
    p = Palette("brewer")
    projection = crs.Mercator()
    cm = BrewerMap(matplotlib).rd_yl_bu(is_qualitative=True, no_of_colors=10)
    fig = plt.figure(figsize=(11, 9))
    ax = plt.subplot(111, projection=projection)
    ax.add_feature(cfeature.BORDERS, alpha=0.5)
    ax.add_feature(cfeature.COASTLINE, alpha=0.5)
    data = get_data()
    shapes = get_shapes()
    for country in shapes:
        ct = country.attributes['ADM0_A3']
        if ct in data:
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=cm(data[ct]),
                              alpha=0.8)
        else:
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=p.gray(shade=30),
                              alpha=0.8)

    # Colorbar
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size="3%", pad=0.2, axes_class=plt.Axes)
    fig.add_axes(ax_cb)

    sm = plt.cm.ScalarMappable(cmap=cm, norm=plt.Normalize(0, 1))
    cb = plt.colorbar(sm, cax=ax_cb)
    cb.ax.set_yticklabels(["{:.1%}".format(i) for i in cb.get_ticks()])
    text = "Percentage of population using at least\nbasic drinking-water " \
           "services in 2017"
    ax.annotate(text,
                xy=(0.95, 0.05), xycoords="axes fraction",
                ha="right", va="bottom",
                fontsize=12,
                bbox=dict(fc=p.white(),
                          pad=12,
                          alpha=0.9))
    ax.annotate(
        "Gray: Data not available.\nData: WHO World Health Statistics",
        xy=(1, -0.02), ha="right",
        xycoords="axes fraction", va="top", color=p.gray())
    plt.savefig("plot.png", dpi=150)
    plt.show()


def run():
    draw_map()

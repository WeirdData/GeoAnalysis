#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#
# Functions related to Rainfall
#
# Data Source:
# Gov of India
# https://data.gov.in/catalog/rainfall-india
# Rajanand Ilangovan
# https://www.kaggle.com/rajanand/rainfall-in-india
#
# Shape file source:
# Shijith Kunhitty
# https://groups.google.com/forum/#!topic/datameet/12L5jtjUKhI

import cartopy.crs as ccrs
import geopandas
import matplotlib
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
from SecretColors import Palette
from SecretColors.cmaps import ColorMap
from matplotlib.animation import FuncAnimation

p = Palette()

color_list = p.blue(no_of_colors=20, starting_shade=30, ending_shade=100)
bm = ColorMap(matplotlib).from_list(color_list, is_qualitative=True)


class MetaDivision:
    """
    Simple class for holding data
    """

    def __init__(self, row):
        self.name = row["ST_NM"]
        self.geometry = row["geometry"]
        self.value = None

    @property
    def color(self):
        if self.value is None:
            return p.gray(shade=30)
        else:
            return bm(self.value)


def generate_divisions():
    """
    Data cleanup function
    """
    shape_file = "data/meterological/indian_met_zones v2.shp"
    df = geopandas.read_file(shape_file)

    # Generate mapping for shape files and actual data
    # This step is necessary because naming standard is not sane in both data
    name_map = list(set(df["ST_NM"].values))
    name_map = {x: x.upper() for x in name_map}

    # Some of the following names have spelling mistakes, however, we will
    # use them because main data is in that format

    name_map["SHWB"] = "SUB HIMALAYAN WEST BENGAL & SIKKIM"
    name_map["Haryana, CHD & Delhi"] = "HARYANA DELHI & CHANDIGARH"
    name_map["Rayalaseema"] = "RAYALSEEMA"
    name_map["N.I. Karnataka"] = "NORTH INTERIOR KARNATAKA"
    name_map["S.I. Karnataka"] = "SOUTH INTERIOR KARNATAKA"
    name_map["Saurashtra & Kachh"] = "SAURASHTRA & KUTCH"
    name_map["Odisha"] = "ORISSA"
    name_map["Andaman & Nicobar Island"] = "ANDAMAN & NICOBAR ISLANDS"
    name_map["Tamil Nadu & Puducherry"] = "TAMIL NADU"
    name_map["NMMT"] = "NAGA MANI MIZO TRIPURA"
    name_map["Marathwada"] = "MATATHWADA"

    divisions = {}
    for _, row in df.iterrows():
        divisions[name_map[row["ST_NM"]]] = MetaDivision(row)
    return divisions


def draw_map(ax, sub):
    for d in sub.values():
        ax.add_geometries([d.geometry],
                          crs=ccrs.PlateCarree(),
                          fc=d.color)


MONTH = {
    0: "JAN", 1: "FEB", 2: "MAR", 3: "APR", 4: "MAY", 5: "JUN",
    6: "JUL", 7: "AUG", 8: "SEP", 9: "OCT", 10: "NOV", 11: "DEC"
}


def animate(y, ax, ax2, sub, df, max_rain):
    """
    Animation function

    :param y: frame index
    :param ax: axes for main figure
    :param ax2: axes for bottom bar
    :param sub: dictionary of our data class
    :param df: Rainfall data
    :param max_rain: Maximum rainfall for normalization
    """
    current_year = 1901 + int(y / 12)
    year_df = df[df["YEAR"] == current_year]
    m = y % 12
    for k in sub.values():
        k.value = None

    total_rainfall = 0
    months = 0
    for _, row in year_df.iterrows():
        months += 1
        value = row[MONTH[m]]
        total_rainfall += value
        sub[row["SUBDIVISION"]].value = value / max_rain

    total_rainfall = total_rainfall / months
    ax.clear()
    ax.annotate(f"{MONTH[m]} {current_year}", (1, 1.01),
                fontsize=12,
                ha="right",
                va="top",
                alpha=0.8,
                bbox=dict(facecolor=p.red(shade=20), edgecolor='none'),
                fontfamily="IBM Plex Mono",
                xycoords='axes fraction')
    draw_map(ax, sub)
    ax.annotate("Rainfall in Meteorological Subdivisions of India",
                (0.5, 1.1),
                fontsize=14,
                ha="center",
                va="center",
                color=p.gray(shade=90),
                fontfamily="IBM Plex Sans",
                xycoords='axes fraction')

    ax.set_extent([67.0, 98.0, 5.0, 38.0], crs=ccrs.PlateCarree())
    ax.axis("off")
    set_bottom_bar(ax2, m, current_year, total_rainfall)


def set_bottom_bar(ax2, current, year, total_rainfall):
    """
    Function to set up bottom month bar

    :param total_rainfall: Total rainfall for the year
    :param ax2: Axes
    :param current: Current month
    :param year: Current year
    """
    # ax2.clear()
    ax2.set_xlim(1, 115)
    # ax2.set_ylim(0, 1)
    ax2.bar(year - 1900, total_rainfall, color=p.red(shade=30), width=1)

    labels = [0, 25, 50, 75, 100, 115]
    ax2.set_xticks(labels)
    ax2.set_xticklabels([x + 1900 for x in labels],
                        fontfamily="IBM Plex Sans",
                        fontweight="light")

    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.set_xlabel("Year", fontfamily="IBM Plex Sans")
    ax2.set_ylabel("Rainfall (mm)", fontsize=9, labelpad=2,
                   fontfamily="IBM Plex Sans", color=p.gray())
    ax2.grid(axis="y", zorder=0, ls="--", color=p.gray())


def run():
    fig = plt.figure(figsize=(8, 8))
    gs = gridspec.GridSpec(8, 8)
    ax = fig.add_subplot(gs[:-2, :], projection=ccrs.PlateCarree())
    ax2 = fig.add_subplot(gs[-2, :])
    ax3 = fig.add_subplot(gs[-1, :])
    sub = generate_divisions()
    df = pd.read_csv("data/rainfall.csv")
    max_rain = df.iloc[:, 2:14]
    max_rain = max(max_rain.max().values)

    ax3.axis("off")
    ax3.annotate("Colors are normalized to highest rainfall amount.\nDarker "
                 "color represents higher rainfall. (Suratekar R. (c) 2020)",
                 (1, -0.1),
                 fontsize=9,
                 color=p.gray(),
                 fontfamily="IBM Plex Sans",
                 xycoords="axes fraction", ha="right")

    ani_object = FuncAnimation(fig=fig,
                               func=animate,
                               frames=range(0, 1380),
                               fargs=(ax, ax2, sub, df, max_rain),
                               repeat=False,
                               interval=1)

    # norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
    # mappable = matplotlib.cm.ScalarMappable(norm=norm, cmap=bm)
    # plt.colorbar(mappable=mappable)

    # Set up formatting for the movie files
    ffmpeg = animation.writers['ffmpeg']
    writer = ffmpeg(metadata=dict(artist='Me'))

    # plt.show()
    ani_object.save('rainfall.mp4', writer=writer)

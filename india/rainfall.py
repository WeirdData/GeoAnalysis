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
import matplotlib.pyplot as plt
import pandas as pd
from SecretColors import Palette
from SecretColors.cmaps import ColorMap, BrewerMap
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec

p = Palette()

color_list = p.blue(no_of_colors=30, starting_shade=30)
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
    for _, row in year_df.iterrows():
        sub[row["SUBDIVISION"]].value = row[MONTH[m]] / max_rain

    ax.clear()
    ax.annotate(f"{MONTH[m]} {current_year}", (1, 1),
                fontsize=14,
                ha="right",
                color=p.gray(shade=70),
                fontfamily="IBM Plex Sans",
                xycoords='axes fraction')
    draw_map(ax, sub)
    ax.set_extent([67.0, 98.0, 5.0, 38.0], crs=ccrs.PlateCarree())
    ax.axis("off")
    set_bottom_bar(ax2, m, current_year)


def set_bottom_bar(ax2, current, year):
    """
    Function to set up bottom month bar

    :param ax2: Axes
    :param current: Current month
    :param year: Current year
    """
    ax2.clear()
    data = [0.2 for _ in range(0, 12)]
    colors = [p.gray_blue(shade=10) for _ in data]
    colors[current] = p.gray_blue(shade=30)
    colors[current - 1] = p.gray_blue(shade=20)
    n = current + 1
    if n > 11:
        n = 0
    colors[n] = p.gray_blue(shade=20)
    ax2.set_xlim(-1, 12)
    ax2.set_ylim(0, 0.8)
    ax2.bar(range(len(data)), data, color=colors)
    ax2.set_xticks(list(range(len(data))))
    ax2.set_xticklabels(list(MONTH.values()),
                        fontfamily="IBM Plex Sans",
                        fontweight="light")
    # ax2.axis("off")
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['bottom'].set_visible(False)
    ax2.set_yticks([])
    ax2.annotate(f"Rainfall in Meteorological Subdivisions of India ({year})",
                 (0.5, 0.5),
                 fontsize=13,
                 fontfamily="IBM Plex Sans",
                 xycoords='axes fraction', ha="center")

    ax2.annotate("Colors are normalized to highest rainfall amount.\nDarker "
                 "color represents higher rainfall. (Suratekar R. (c) 2020)",
                 (0.95, -0.8),
                 fontsize=9,
                 color=p.gray(),
                 fontfamily="IBM Plex Sans",
                 xycoords="axes fraction", ha="right")


def run():
    fig = plt.figure(figsize=(8, 8))
    gs = gridspec.GridSpec(6, 6)
    ax = fig.add_subplot(gs[:-1, :], projection=ccrs.PlateCarree())
    ax2 = fig.add_subplot(gs[-1, :])
    sub = generate_divisions()
    df = pd.read_csv("data/rainfall.csv")
    max_rain = df.iloc[:, 2:14]
    max_rain = max(max_rain.max().values)

    ani_object = FuncAnimation(fig=fig,
                               func=animate,
                               frames=range(0, 1380),
                               fargs=(ax, ax2, sub, df, max_rain),
                               repeat=False,
                               interval=10)

    # norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
    # mappable = matplotlib.cm.ScalarMappable(norm=norm, cmap=bm)
    # plt.colorbar(mappable=mappable)

    # Set up formatting for the movie files
    ffmpeg = animation.writers['ffmpeg']
    writer = ffmpeg(metadata=dict(artist='Me'))

    plt.show()
    # ani_object.save('rainfall.mp4', writer=writer)

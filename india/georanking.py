#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#
#  Bounding Box for India on PlateCarree scale = [67.0, 98.0, 5.0, 38.0]
#  Shape file downloaded from : https://www.diva-gis.org/gdata
#  Data is not included here because of restrictive license
#
#  To get disputed areas near Pakistan and China, Old administrative area is
#  added. Shape file was taken from : https://bit.ly/3aklP75

from typing import Dict

import cartopy.crs as ccrs
import geopandas
import matplotlib.pyplot as plt
from SecretColors import Palette
from SecretColors.utils import text_color

from india.constants import STATE_COLUMN, JKL_NAME
from india.model import State

p = Palette()


def _draw_states(ax: plt.Axes, states: Dict[str, State]):
    for s in states.values():
        ax.add_geometries([s.shape], crs=ccrs.PlateCarree(),
                          facecolor=s.color,
                          edgecolor=p.gray(shade=60))
        if s.show_label:
            ax.text(s.label_x, s.label_y, s.name,
                    transform=ccrs.PlateCarree(),
                    color=text_color(s.color),
                    size=8, rotation=s.label_rotation,
                    ha='center', va='center')


def _get_jkl():
    filename = "data/extra/Indian_States.shp"
    df = geopandas.read_file(filename)
    df = df[df["st_nm"] == "Jammu & Kashmir"].reset_index(drop=True)
    df = df.rename(columns={"st_nm": STATE_COLUMN})
    df.iloc[0, 0] = JKL_NAME
    for _, row in df.iterrows():
        return State(row)


def _fetch_maps():
    filename = "data/India/IND_adm1.shp"
    df = geopandas.read_file(filename)
    ax = plt.axes(projection=ccrs.PlateCarree())  # type:plt.Axes
    states = {JKL_NAME: _get_jkl()}

    for index, row in df.iterrows():
        s = State(row)
        if s.name != "Jammu and Kashmir":
            states[s.name] = s

    _draw_states(ax, states)
    ax.set_extent([67.0, 98.0, 5.0, 38.0], crs=ccrs.PlateCarree())
    ax.axis("off")
    plt.gcf().set_size_inches(7, 7)
    plt.savefig("plot.png", dpi=300)


def run():
    _fetch_maps()

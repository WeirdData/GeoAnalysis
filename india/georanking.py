#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#
#  Bounding Box for India on PlateCarree scale = [67.0, 98.0, 5.0, 38.0]
#  Shape file downloaded from : https://www.diva-gis.org/gdata
#  Data is not included here because of restrictive license
#
#  To get disputed areas near Pakistan and China, Old administrative area is
#  added. Shape file was taken from : https://bit.ly/3aklP75

import re
from typing import Dict

import cartopy.crs as ccrs
import geopandas
import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from SecretColors import Palette, ColorMap

from india.constants import STATE_COLUMN, JKL_NAME
from india.model import State

p = Palette(show_warning=False)
# cm = matplotlib.cm.get_cmap('viridis_r')
cols = p.ultramarine(no_of_colors=10)
cols.extend(p.green(no_of_colors=20))
cols.extend(p.magenta(no_of_colors=20))
cm = ColorMap(matplotlib, p).from_list(cols, is_qualitative=True)
TOTAL_POPULATION = 1210569573


def _draw_states(ax: plt.Axes, states: Dict[str, State]):
    for s in states.values():
        color = cm(s.mapped_value)
        ax.add_geometries([s.shape], crs=ccrs.PlateCarree(),
                          facecolor=color,
                          edgecolor=p.gray(shade=60))
        tx_color = p.black()
        if s.name in ["Uttar Pradesh", "Delhi"]:
            tx_color = p.white()
        if s.show_label:
            ax.text(s.label_x, s.label_y, s.mapped_label,
                    transform=ccrs.PlateCarree(),
                    color=tx_color,
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


def draw_with_mapping(mapping):
    filename = "data/India/IND_adm1.shp"
    df = geopandas.read_file(filename)
    fig = plt.figure(figsize=(7, 7))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    states = {JKL_NAME: _get_jkl()}
    for index, row in df.iterrows():
        s = State(row)
        if s.name == "Orissa":
            s._name = "Odisha"
        elif s.name == "Uttaranchal":
            s._name = "Uttarakhand"
        elif s.name == "Daman and Diu":
            continue
        if s.name != "Jammu and Kashmir":
            states[s.name] = s

    for s in states.values():
        if s.name == JKL_NAME:
            s.mapped_label = mapping["Jammu and Kashmir"][0]
            s.mapped_value = mapping["Jammu and Kashmir"][1] / TOTAL_POPULATION
            continue
        elif s.name == "Daman and Diu":
            continue
        s.mapped_label = mapping[s.name][0]
        s.mapped_value = mapping[s.name][1] / TOTAL_POPULATION

    _draw_states(ax, states)
    norm = mpl.colors.Normalize(vmin=0, vmax=100)
    sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
    sm.set_array([])
    # cbar = plt.colorbar(sm, ticks=np.linspace(0, 100, 10),
    #                     fraction=0.046,
    #                     pad=0.04)
    ax.set_extent([67.0, 98.0, 5.0, 38.0], crs=ccrs.PlateCarree())
    ax.axis("off")
    plt.savefig("plot.png", dpi=300)


def get_population_mapping():
    """
    World population data is from Kaggle:
    https://www.kaggle.com/tanuprabhu/population-by-country-2020

    Population of Indian States is simply copy paste from Wikipedia
    (Both Datasets accessed on 17 August 2020)
    """
    world = pd.read_csv("data/population.csv")
    states = pd.read_csv("data/states.csv")
    states = dict(
        zip(states["State or union territory "], states["Population "]))

    states = [(x.strip(), int(re.sub("[^0-9]", "", states[x]))) for x in
              states]

    world = dict(
        zip(world["Country (or dependency)"], world["Population (2020)"]))
    world = [(str(x).strip(), int(re.sub("[^0-9]", "", str(world[x])))) for x
             in world]

    states = sorted(states, key=lambda x: x[1], reverse=True)
    world = sorted(world, key=lambda x: x[1], reverse=True)
    mapping = {}
    current_state = states[0]
    for w in world:
        if current_state[1] >= w[1]:
            mapping[current_state[0]] = (w[0], current_state[1])
            try:
                states.pop(0)
                current_state = states[0]
            except IndexError:
                break

    return mapping


def run():
    mapping = get_population_mapping()
    draw_with_mapping(mapping)

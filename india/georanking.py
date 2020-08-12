#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#
#  Bounding Box for India on PlateCarree scale = [67.0, 98.0, 5.0, 38.0]
#  Shape file downloaded from : https://www.diva-gis.org/gdata

import cartopy.crs as ccrs
import geopandas
import matplotlib.pyplot as plt
import pandas as pd
from SecretColors import Palette

p = Palette()


def _draw_state(ax: plt.Axes, data: pd.DataFrame):
    poly = data['geometry']
    state = data['NAME_1']
    # x = poly.centroid.x
    # y = poly.centroid.y
    print(state)
    ax.add_geometries([poly], crs=ccrs.PlateCarree(),
                      facecolor=p.blue(shade=30),
                      edgecolor=p.blue(shade=60))

    # ax.text(x, y, state, size=9, ha='center', va='center',
    #         transform=ccrs.PlateCarree())


def _fetch_maps():
    resolution = '10m'
    category = 'cultural'
    name = 'admin_1_states_provinces'

    # shpfilename = shapereader.natural_earth(resolution, category, name)
    shpfilename = "data/IND_adm1.shp"
    # read the shapefile using geopandas
    df = geopandas.read_file(shpfilename)
    ax = plt.axes(projection=ccrs.PlateCarree())
    for index, row in df.iterrows():
        _draw_state(ax, row)

    ax.set_extent([67.0, 98.0, 5.0, 38.0], crs=ccrs.PlateCarree())
    plt.show()


def run():
    _fetch_maps()

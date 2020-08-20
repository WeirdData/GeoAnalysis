#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#
#  Bounding Box for India on PlateCarree scale = [67.0, 98.0, 5.0, 38.0]
#  Shape file downloaded from : https://www.diva-gis.org/gdata
#  Data is not included here because of restrictive license
#
#  To get disputed areas near Pakistan and China, Old administrative area is
#  added. Shape file was taken from : https://bit.ly/3aklP75

import json
from india.model import StateMap
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt
import cartopy.io.shapereader as shpreader
import geopandas


def plot_suicide_data():
    """
    Data is taken from [on 20 August 2020]
    https://data.gov.in/resources/stateut-wise-incidence-and-rate-suicides-during-2017
    Reference URL:
    https://ncrb.gov.in/accidental-deaths-suicides-in-india
    """
    with open("data/other/suicide.json") as f:
        data = json.loads(f.read())

    states = []
    for d in data['data']:
        states.append(StateMap(d[2], d[-1]))

    states = [x for x in states if x.is_valid]

    filename = "data/India/IND_adm1.shp"
    df = geopandas.read_file(filename)


    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.add_feature(cf.COASTLINE)
    ax.add_feature(cf.BORDERS)
    ax.add_feature(cf.LAND)
    ax.add_feature(cf.OCEAN)
    ax.set_extent([67.0, 98.0, 5.0, 38.0], crs=ccrs.PlateCarree())
    # plt.show()


def run():
    plot_suicide_data()

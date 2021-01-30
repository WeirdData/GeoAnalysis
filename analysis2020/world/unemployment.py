#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#  Analysis related to world unemployment data
#  Data Source: https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS

import cartopy.crs as crs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from SecretColors import Palette
from SecretColors.cmaps import BrewerMap
from matplotlib.animation import FuncAnimation

p = Palette()
cm = BrewerMap(matplotlib).pu_rd(is_qualitative=True)


def draw_map(i, ax, countries):
    ax.clear()
    year = i + 2000
    data = get_data(year)
    if len(data) == 0:
        return
    max_um = max(data.values())
    ax.add_feature(cfeature.OCEAN, color=p.blue(shade=30))
    ax.add_feature(cfeature.BORDERS, alpha=0.5)
    ax.add_feature(cfeature.COASTLINE, alpha=0.5)

    for country in countries:
        ct = country.attributes['ADM0_A3']
        if ct in data.keys():
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=cm(data[ct] / max_um))
        else:
            ax.add_geometries([country.geometry], crs.PlateCarree(),
                              fc=p.gray(shade=20),
                              ec=p.gray(shade=50),
                              hatch='\\\\\\',
                              alpha=0.3)

    ax.annotate(f"{year}", (1.01, 1.02),
                fontsize=14,
                xycoords="axes fraction")


def get_data(year: int):
    df = pd.read_csv("data/unemployment/unemployment.csv")
    df = df.fillna(np.inf)
    data = {x[0]: x[1] for x in zip(df["Country Code"], df[str(year)]) if x[
        1] != np.inf}
    return data


def run():
    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1, projection=crs.PlateCarree())

    norm = matplotlib.colors.Normalize(vmin=0,
                                       vmax=1)
    sm = plt.cm.ScalarMappable(cmap=cm, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax,
                        pad=0.02,
                        ticks=np.linspace(0, 1, 10),
                        shrink=0.5, extend="both")
    cbar.ax.set_ylabel("% of total labor force")

    ani_object = FuncAnimation(fig=fig,
                               func=draw_map,
                               frames=range(0, 19),
                               fargs=(ax, countries),
                               repeat=False,
                               interval=20)

    # plt.title(f"Unemployment in {year} (modeled ILO estimate)", pad=10)
    ffmpeg = animation.writers['ffmpeg']
    writer = ffmpeg(metadata=dict(artist='Me'))

    plt.show()
    # ani_object.save('unemployment.mp4', writer=writer)

#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#  Distances analysis
#  Projection code is borrowed from
#  https://stackoverflow.com/questions/52105543/drawing-circles-with-cartopy-in-orthographic-projection

import cartopy.crs as crs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from SecretColors import Palette
from shapely.geometry import Point

palette = Palette()


def __extract(points, index):
    p_min, p_max = None, None
    for p in points:
        if p_min is None:
            p_min = p
        if p_max is None:
            p_max = p
        if p_min[index] <= p[index]:
            p_min = p
        elif p_max[index] >= p[index]:
            p_max = p
    return p_min, p_max


def extreme_points(name: str):
    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()
    for country in countries:
        ct = country.attributes['ADM0_A3']
        if ct == name:
            points = country.geometry.boundary.coords
            x_min, x_max = __extract(points, 0)
            y_min, y_max = __extract(points, 1)
            return x_min, y_min, x_max, y_max


def compute_radius(ortho, lat, lon, radius_degrees):
    phi1 = lat + radius_degrees if lat <= 0 else lat - radius_degrees
    _, y1 = ortho.transform_point(lon, phi1, crs.PlateCarree())
    return abs(y1)


def india_seul():
    xmin, ymin, xmax, ymax = extreme_points("IND")
    lat = xmin[1]
    lon = xmin[0]
    r = (ymin[1] - ymax[1])

    cape = (ymax[0], ymax[1])
    seul = (126.58, 37.34)

    proj = crs.Orthographic(central_longitude=lon, central_latitude=lat)
    r_ortho = compute_radius(proj, lat, lon, r)
    r_center = compute_radius(proj, lat, lon, 0.5)
    pad_radius = compute_radius(proj, lat, lon, r + 10)
    width = 800
    height = 800
    dpi = 150
    fig = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    ax.set_xlim([-pad_radius, pad_radius])
    ax.set_ylim([-pad_radius, pad_radius])

    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.BORDERS)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.OCEAN)

    ax.add_patch(
        mpatches.Circle(xy=(lon, lat), radius=r_center,
                        color=palette.red(), transform=proj,
                        zorder=40))
    ax.add_patch(
        mpatches.Circle(xy=(lon, lat), radius=r_ortho, alpha=0.3,
                        color=palette.red(shade=40),
                        transform=proj, zorder=30))

    ax.add_patch(
        mpatches.Circle(xy=seul, radius=0.5,
                        color=palette.red(),
                        transform=crs.PlateCarree(),
                        zorder=40))

    ax.add_patch(
        mpatches.Circle(xy=cape, radius=0.5,
                        color=palette.red(),
                        transform=crs.PlateCarree(),
                        zorder=40))

    ax.text(seul[0] - 3, seul[1], "Seoul, South Korea",
            transform=crs.PlateCarree(),
            bbox=dict(facecolor=palette.white()), zorder=60, ha="right",
            va="bottom")
    ax.text(lon + 2, lat, "Kibithoo, India", transform=crs.PlateCarree(),
            zorder=60,
            bbox=dict(facecolor=palette.white()), ha="left")
    ax.text(cape[0] + 2, cape[1], "Cape Comorin, India",
            transform=crs.PlateCarree(), zorder=60,
            va="top", ha="left", bbox=dict(facecolor=palette.white()))

    ax.gridlines(color=palette.blue(shade=30), zorder=1)
    plt.tight_layout()
    plt.savefig("plot.png")
    plt.show()


def run():
    india_seul()

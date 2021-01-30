#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#

import yaml

from india.models import *

data = {
    "IN-AP": ["known as kohinoor of india"],
    "IN-AR": ["called arunachal pradesh"],
    "IN-AS": ["unique"],
    "IN-BR": ["so backward"],
    "IN-CT": ["called the herbal state"],
    "IN-GA": ["carnival celebrated"],
    "IN-GJ": ["a dry state"],
    "IN-HR": ["day celebrated"],
    "IN-HP": ["called himachal"],
    "IN-JH": ["poor"],
    "IN-KA": ["known as the land of sandalwood"],
    "IN-KL": ["called god's own country"],
    "IN-MP": ["a backward and poor state"],
    "IN-MH": ["worst hit by coronavirus"],
    "IN-MN": ["called the jewel of india"],
    "IN-ML": ["called the abode of clouds"],
    "IN-MZ": ["called molasses basin"],
    "IN-NL": ["called the land of festivals"],
    "IN-OR": ["prone to cyclones"],
    "IN-PB": ["called the gateway of india"],
    "IN-RJ": ["called the desert state of india"],
    "IN-SK": ["considered as a biodiversity hotspot"],
    "IN-TN": ["against hindi"],
    "IN-TG": ["separated from andhra pradesh"],
    "IN-TR": ["called a landlocked state"],
    "IN-UP": ["so dangerous"],
    "IN-UT": ["called devbhoomi"],
    "IN-WB": ["in east"],
    "IN-AN": ["called an archipelago"],
    "IN-CH": ["unlikely to be affected by a cyclone"],
    "IN-DD": ["a union territory"],
    "IN-DL": ["so polluted"],
    "IN-LK": ["known as a coral island"],
    "IN-JK": ["thinly populated"],
    "IN-LD": ["called the land of high passes"],
    "IN-PY": ["a union territory"]
}


def map_data(states: Dict[str, State], ax: plt.Axes = None):
    p = Palette()
    for s in states.values():
        if s.iso in data:
            s.color = p.blue(shade=20)
            # txt = data[s.iso][0]
            # txt = txt[:10] + "\n" + txt[10:]
            # ax.text(s.x, s.y,
            #         txt
            #         , ha="center",
            #         va="center")


def prepare_map():
    p = Palette()
    with open("india/states.yml") as f:
        meta = yaml.load(f, Loader=yaml.SafeLoader)

    # plt.figure(figsize=(10, 8))
    mp = IndianMap()
    sts = mp.generate_states(meta)
    current_y = 1
    crs = ccrs.PlateCarree()
    transform = crs._as_mpl_transform(mp.ax)
    data_to_axis = mp.ax.transAxes
    for s in sts.values():
        mp.ax.add_geometries([s.geometry],
                             fc=p.blue(shade=15),
                             ec=p.blue(shade=30),
                             crs=ccrs.PlateCarree())

        if current_y == 0:
            continue
        mp.ax.annotate("some long sentence", xytext=(0, current_y),
                       xy=data_to_axis.transform((s.x, s.y)),
                       arrowprops=dict(facecolor='black'),
                       xycoords="axes fraction",
                       ha='right', va='top')
        break
        current_y -= 0.1

    mp.ax.set_extent(mp.extent, crs=ccrs.PlateCarree())

    mp.ax.set_frame_on(False)

    # plt.savefig("plot.png", dpi=150, transparent=True)
    plt.show()


def run():
    prepare_map()

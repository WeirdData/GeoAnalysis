#  WeirdData Copyright (c) 2021.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#  Data Source: https://en.wikipedia.org/wiki/List_of_female_Indian_chief_ministers
import yaml

from india.models import *

ALL_DATA = ["Uttar Pradesh", "Odisha", "Goa", "Assam", "Tamil Nadu", "Punjab",
            "Bihar", "Delhi", "Madhya Pradesh", "Rajasthan", "West Bengal",
            "Gujarat", "Jammu and Kashmir"]


def map_data(data, states: Dict[str, State], ax: plt.Axes = None):
    p = Palette("brewer")
    for s in states.values():
        if s.name in data:
            s.color = p.green(shade=40)
        else:
            s.color = p.gray(shade=20)


def draw_map():
    with open("india/states.yml") as f:
        meta = yaml.load(f, Loader=yaml.SafeLoader)

    plt.figure(figsize=(10, 8))
    mp = IndianMap()
    sts = mp.generate_states(meta)
    map_data(ALL_DATA, sts, mp.ax)
    mp.draw()
    plt.title("States with at least one female Chief Minister (1947-2020)")
    plt.savefig("plot.png", dpi=150)
    plt.show()


def run():
    draw_map()

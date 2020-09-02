#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#


import yaml

from india.models import *


def map_data(states: Dict[str, State], ax: plt.Axes = None):
    p = Palette()
    for s in states.values():
        if s.name == "Maharashtra":
            s.color = p.red(shade=30)
            ax.text(s.x, s.y, "55%", ha="center", va="center")


def prepare_map():
    with open("india/states.yml") as f:
        meta = yaml.load(f, Loader=yaml.SafeLoader)

    plt.figure(figsize=(10, 8))
    mp = IndianMap()
    sts = mp.generate_states(meta)
    map_data(sts, mp.ax)
    mp.draw()
    plt.show()


def run():
    prepare_map()

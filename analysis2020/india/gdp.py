#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#  Data :
#  https://en.wikipedia.org/wiki/List_of_Indian_states_and_union_territories_by_GDP

import csv
import yaml

from india.models import *


def get_data():
    data = {}
    with open("data/state_gdp.csv") as f:
        for row in csv.reader(f):
            data[row[1]] = float(row[2].split(" ")[0][1:])
    return data


no_data = ["Dadra and Nagar Haveli and Daman and Diu", "Lakshadweep"]


def map_data(data, states: Dict[str, State], ax: plt.Axes = None):
    p = Palette()
    for s in states.values():
        if s.name in no_data:
            s.color = p.gray()
        else:
            if s.name in data:
                s.color = p.red(shade=30)
            else:
                s.color = p.blue(shade=30)


def draw_map():
    with open("india/states.yml") as f:
        meta = yaml.load(f, Loader=yaml.SafeLoader)

    plt.figure(figsize=(10, 8))
    mp = IndianMap()
    sts = mp.generate_states(meta)
    data = get_data()
    data = split_states(data)
    data = [x[0] for x in data[:11]]
    map_data(data, sts, mp.ax)
    mp.draw()
    plt.savefig("plot.png", dpi=150)
    plt.show()


def split_states(data):
    pop = {}

    def _remove(x):
        return int("".join([x for x in list(x) if str(x).isnumeric()]))

    with open("data/states.csv") as f:
        next(f)
        next(f)
        for row in csv.reader(f):
            pop[row[1].strip()] = _remove(row[2]) / 1000

    number = 11
    tmp = [(x, data[x] / pop[x]) for x in data]
    tmp = sorted(tmp, key=lambda x: x[1], reverse=True)
    top_list = [x[1] for x in tmp[:number]]
    others = [x[1] for x in tmp[number:]]
    print(sum(top_list), sum(others))
    print(sum(top_list) * 100 / (sum([sum(top_list), sum(others)])))
    print(tmp)
    return tmp


def run():
    data = get_data()
    split_states(data)
    # draw_map()

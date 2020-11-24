#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#  2019 Tea Export (in USD)
#  Data from : http://www.worldstopexports.com/tea-exports-by-country/

import cartopy.crs as crs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import pandas as pd
from SecretColors import Palette

p = Palette('brewer')


def get_data():
    df = pd.read_csv("data/tea.csv", header=None,
                     names=["No", "Country", "Export(USD)", "Change"])

    df['Country'] = df['Country'].str.lower()
    df = df.set_index("Country")
    codes = pd.read_csv('data/country-codes.csv')
    codes['name'] = codes['name'].str.lower()
    codes = codes.set_index("name")
    codes = codes[["Alpha-3 code"]]
    codes = codes.dropna()
    df = pd.concat([df, codes], axis=1)
    df = df.dropna(subset=["Alpha-3 code", "Export(USD)"])
    df["Export(USD)"] = df["Export(USD)"] \
        .map(lambda x: int(str(x).replace("$", "").replace(",", "")))

    c_map = dict(zip(df["Alpha-3 code"], df["Export(USD)"]))
    return c_map


def draw_map():
    # Generate counts before drawing the map
    counts = get_data()

    plt.figure(figsize=(12, 9))
    ax = plt.subplot(111, projection=crs.Miller())

    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()
    # ax.add_feature(cfeature.OCEAN, color=p.blue(shade=30))
    ax.add_feature(cfeature.BORDERS, alpha=0.5)
    ax.add_feature(cfeature.COASTLINE, alpha=0.5)
    max_count = max(counts.values())
    counts = {x: counts[x] / max_count for x in counts}
    cmap = data_calculations()
    for country in countries:
        ct = country.attributes['ADM0_A3']
        if ct in counts:
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=cmap[ct],
                              alpha=0.8)
        else:
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=p.gray(shade=20),
                              alpha=0.8)

    plt.title("70% of the World's Tea Export in 2019")
    plt.savefig("plot.png", dpi=300)
    plt.show()


def split_equal(numbers, groups):
    numbers = sorted(numbers, key=lambda x: x[1], reverse=True)
    final_groups = [[] for _ in range(groups)]
    index_group = [[] for _ in range(groups)]
    max_sum = [0 for _ in range(groups)]
    while len(numbers) > 0:
        idx = max_sum.index(min(max_sum))
        final_groups[idx].append(numbers[0][1])
        index_group[idx].append(numbers[0][0])
        max_sum[idx] = sum(final_groups[idx])
        numbers.pop(0)

    print([sum(x) for x in final_groups])
    return index_group


def split_from_top(numbers):
    final_groups = []
    labels = []
    tmp = []
    tmp_labels = []
    while len(numbers) > 0:
        if sum(tmp) >= 70:
            final_groups.append(tmp)
            labels.append(tmp_labels)
            print([round(x, 1) for x in tmp])
            tmp = []
            tmp_labels = []

        tmp.append(numbers[0][1])
        tmp_labels.append(numbers[0][0])
        numbers.pop(0)
    final_groups.append(tmp)
    print([sum(x) for x in final_groups])
    labels.append(tmp_labels)
    return labels


def data_calculations():
    data = get_data()
    total = sum(data.values())
    data = [(k, v * 100 / total) for k, v in data.items()]
    data = sorted(data, key=lambda x: x[1], reverse=True)
    # groups = split_equal(data, 2)
    groups = split_from_top(data)
    colors = [p.orange(shade=40),
              p.gray(shade=20),
              p.green(shade=40)]
    color_map = {}
    for i in range(len(groups)):
        for c in groups[i]:
            if i == 0:
                print(c)
            color_map[c] = colors[i]

    return color_map


def plot_top():
    data = get_data()
    color_map = data_calculations()
    data = [(k, v) for k, v in data.items()]
    data = sorted(data, key=lambda x: x[1], reverse=True)
    total = sum([x[1] for x in data])
    values = [x[1] * 100 / total for x in data][:5]
    labels = [x[0] for x in data][:5]
    print(values)
    for i in range(len(values)):
        plt.barh(i, values[i], color=color_map[labels[i]])
    plt.yticks(range(len(values)), labels)
    plt.xlabel("% of world export")
    ax = plt.gca()  # type:plt.Axes
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig("plot.png", dpi=300, transparent=True)
    plt.show()


def run():
    draw_map()

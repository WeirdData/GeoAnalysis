#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#  Data from
#  https://www.alltime-athletics.com


from collections import Counter, defaultdict

import cartopy.crs as crs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from SecretColors import Palette
from SecretColors.cmaps import TableauMap
from scipy.stats import gaussian_kde

p = Palette()
color_shades = [20, 30, 40, 50]
colors = [p.green(shade=x) for x in color_shades]
cm = TableauMap(matplotlib).from_list(colors)


def get_data(filename):
    c = 0
    data = []
    ctr = Counter()
    with open(filename) as f:
        for line in f:
            line = line.strip().split(" ")
            line = [x for x in line if len(x) > 0]
            time = float(line[1].replace("A", ""))
            name = ""
            for k in line[3:]:
                if k == k.upper() and len(k) == 3:
                    country = k
                    break
                else:
                    name += f"{k} "

            date = line[-1]
            name = name.strip()
            data.append((time, name, country, date))
            if c < 10:
                ctr.update({country})
            if c == 2000:
                break
            c += 1

    return data


def run_time():
    plt.rcParams['axes.facecolor'] = p.gray(shade=10)
    fig = plt.figure(figsize=(10, 7))
    ax1 = fig.add_subplot(1, 1, 1)
    men_data = get_data("data/running/men_100m.tsv")
    women_data = get_data("data/running/women_100m.tsv")
    year_men = [int(x[-1].split(".")[-1]) for x in men_data]
    year_women = [int(x[-1].split(".")[-1]) for x in women_data]
    men = [x[0] for x in men_data]
    women = [x[0] for x in women_data]
    ax1.hist(men, 30, color=p.cyan(shade=40), label="Men", zorder=3)
    ax1.hist(women, 30, color=p.magenta(shade=40), label="Women", zorder=3)
    ax1.set_xlabel("Record Time (in seconds)")
    ax1.set_ylabel("Frequency")
    ax1.set_title("Top 2000 world records for 100 m running", pad=20)
    ax1.legend(loc='upper center', bbox_to_anchor=(0.65, 0.51),
               fancybox=True, ncol=2)
    ax1.annotate(f"Fastest Man ({men[0]} s)\n{men_data[0][1]}",
                 xy=(men[0], 10),
                 xytext=(men[0], 100),
                 ha="left",
                 arrowprops=dict(arrowstyle="->"),
                 zorder=3)
    ax1.annotate(f"Fastest Women ({women[0]} s)\n{women_data[0][1]}",
                 xy=(women[0], 10), xytext=(women[0], 100),
                 arrowprops=dict(arrowstyle="->"), ha="center",
                 zorder=3)
    ax1.annotate("Bottlenose Dolphins\n(10.28 s)",
                 xy=(10.3, 10), xytext=(10.3, 50),
                 arrowprops=dict(arrowstyle="->"), ha="center",
                 zorder=3)
    ax1.annotate("Gentoo\nPenguine (10 s)",
                 xy=(10, 10), xytext=(9.9, 60),
                 arrowprops=dict(arrowstyle="->"),
                 zorder=3, ha="right")
    ax1.annotate("RoadRunner\n(11.26 s)",
                 xy=(11.15, 10), xytext=(10.8, 50),
                 arrowprops=dict(arrowstyle="->"), ha="right",
                 zorder=3)
    ax1.grid(zorder=0, ls="--", color=p.gray(shade=30))

    left, bottom, width, height = [0.15, 0.7, 0.15, 0.15]
    ax2 = fig.add_axes([left, bottom, width, height])
    density_men = gaussian_kde(year_men)
    density_women = gaussian_kde(year_women)
    xs = np.linspace(min(year_men), max(year_men), 200)
    ax2.plot(xs, density_men(xs), color=p.cyan())
    ax2.plot(xs, density_women(xs), color=p.magenta())
    ax2.annotate("Year-wise\nRecords", (0.06, 0.7),
                 xycoords="axes fraction",
                 fontsize=9)
    ax2.set_xlim([min(year_men), max(year_men)])
    ax2.set_xticks(
        [min(year_men),
         min(year_men) + int(max(year_men) / 2 - min(year_men) / 2),
         max(year_men)])
    ax2.set_yticks([])
    ax2.tick_params(axis='both', which='major', labelsize=9)

    left, bottom, width, height = [0.43, 0.48, 0.4, 0.4]
    ax3 = fig.add_axes([left, bottom, width, height],
                       projection=crs.Robinson())
    draw_map(ax3)

    plt.savefig("plot.png", dpi=300)
    plt.show()


def draw_map(ax):
    men_data = get_data("data/running/men_100m.tsv")
    women_data = get_data("data/running/women_100m.tsv")
    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()
    # ax.add_feature(cfeature.OCEAN, color=p.blue(shade=30))
    ax.add_feature(cfeature.BORDERS, alpha=0.1)
    ax.add_feature(cfeature.COASTLINE, alpha=0.5)

    data = Counter([(x[1], x[2]) for x in men_data[:100]])
    data.update([(x[1], x[2]) for x in women_data[:100]])
    tmp = defaultdict(int)
    for d in data:
        tmp[d[1]] += 1
    data = {x: tmp[x] / max(tmp.values()) for x in tmp}
    for country in countries:
        ct = country.attributes['ADM0_A3']
        if ct in data:
            ax.add_geometries([country.geometry],
                              crs.PlateCarree(),
                              fc=cm(data[ct]),
                              alpha=0.8)

    ax.set_title("Countries with most records", fontsize=9)


def run():
    run_time()

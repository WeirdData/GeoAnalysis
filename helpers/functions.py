#  WeirdData Copyright (c) 2021.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#  Helper functions to get around the conversions

import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as crs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import matplotlib
import matplotlib.pyplot as plt


def country_codes(country_lists):
    df = pd.read_csv("helpers/synonym_countries.csv")
    df_2 = df["name"].to_list()
    new_con = [x for x in country_lists if x not in df_2]
    if len(new_con) > 0:
        print("Following new countries found")
        print(new_con)
        raise Exception("Please resolve new countries before proceeding")

    df = dict(zip(df["name"], df["code"]))
    return {x: df[x] for x in country_lists}


def get_shapes():
    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')
    return shpreader.Reader(shpfilename).records()

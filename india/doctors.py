#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#  Web: https://github.com/WeirdData/GeoAnalysis
#
#  Doctors in position at Primary Health Centres in Rural Areas
#  Data from:
#  https://data.gov.in/resources/stateut-wise-doctors-primary-health-centres-rural-areas-during-2005-and-2019

import json
import pandas as pd
from pprint import pprint


def get_data():
    with open("data/doctors.json") as f:
        data = json.load(f)

    columns = {}
    values = []
    c = 0
    for d in data:
        for k in data[d]:
            if isinstance(k, dict):
                columns[c] = k['label']
                c += 1
            else:
                values.append(k)

    df = pd.DataFrame(data=values)
    pprint(columns)
    df = df[[1, 4, 9]]
    print(df)


def run():
    get_data()

from typing import Union

import pandas as pd
from SecretColors import Palette
from geopandas.geoseries import GeoSeries
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon

from india.constants import *


class State:
    def __init__(self, data: pd.DataFrame):
        self._data = data
        self._name = data[STATE_COLUMN]
        self._geometry = data['geometry']
        self.color = Palette().gray(shade=20)
        self.show_label = True

    @property
    def shape(self) -> Union[Polygon, MultiPolygon]:
        if isinstance(self._geometry, GeoSeries):
            return self._geometry.iloc[0]
        else:
            return self._geometry

    def _x(self):
        try:
            off = OFFSETS[self.name][O_X]
        except KeyError:
            off = 0
        return self.shape.centroid.x + off

    def _y(self):
        try:
            off = OFFSETS[self.name][O_Y]
        except KeyError:
            off = 0
        return self.shape.centroid.y + off

    def _r(self):
        try:
            return OFFSETS[self.name][O_R]
        except KeyError:
            return 0

    @property
    def label_x(self):
        return self._x()

    @property
    def label_y(self):
        return self._y()

    @property
    def label_rotation(self):
        return self._r()

    @property
    def name(self) -> str:
        return self._name

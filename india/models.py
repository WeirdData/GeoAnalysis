#  WeirdData Copyright (c) 2020.
#  Author: Rohit Suratekar
#
#  Bounding Box for India on PlateCarree scale = [67.0, 98.0, 5.0, 38.0]
#  Shape file downloaded from : https://www.diva-gis.org/gdata
#  Data is not included here because of restrictive license
#
#  To get disputed areas near Pakistan and China, Old administrative area is
#  added. Shape file was taken from : https://bit.ly/3aklP75

import os
import warnings
from typing import Dict

import cartopy.crs as ccrs
import geopandas
import matplotlib.pyplot as plt
from SecretColors import Palette
from shapely.geometry.multipolygon import MultiPolygon
from shapely.geometry.polygon import Polygon
from typing import Union

palette = Palette()


class State:
    STATES = "States"
    SYN = "Synonymous"

    def __init__(self, name: str, meta: dict = None):
        self._name = name
        self.meta = meta
        self.geometry = None  # type: Union[Polygon, MultiPolygon]
        self.color = palette.ultramarine(shade=40)
        self._label = None
        self.value = 0
        self.show_label = False

    def _get_name(self):
        # If meta file is not provided, just return the name
        if self.meta is None:
            return self._name
        # If meta file is provided, check the details
        # If it is present in the meta data file, return it
        if self._name in self.meta[State.STATES]:
            return self._name
        # If not present, check for the synonymous
        if self._name in self.meta[State.SYN]:
            return self.meta[State.SYN][self._name]
        return None

    @property
    def x(self):
        return self.geometry.centroid.x

    @property
    def y(self):
        return self.geometry.centroid.y

    @property
    def name(self) -> str:
        return self._get_name()

    @property
    def label(self):
        if self._label is None:
            if self.meta is None:
                self._label = self.name
            elif "short" in self.meta[self.STATES][self.name].keys():
                self._label = self.meta[self.STATES][self.name]["short"]
            else:
                self._label = self.name
        return self._label

    @label.setter
    def label(self, value: str):
        self._label = value

    @property
    def iso(self):
        if self.meta:
            return self.meta[self.STATES][self.name]["code"]
        return "N/A"

    @property
    def is_valid(self) -> bool:
        if self.meta is None:
            return True
        else:
            return self.name is not None


class IndianMap:
    COL_STATE = "NAME_1"
    COL_COLOR = "color"
    COL_GEOMETRY = "geometry"

    def __init__(self, level: int = 1):
        self.filename = f"data/India/IND_adm{level}.shp"
        self.override_jk = True
        self._states = {}
        self.jk_file = "data/extra/Indian_States.shp"
        self.level = level
        self._df = None
        self._ax = None
        self.show_label = False
        self.extent = [67.0, 98.0, 5.0, 38.0]

    @property
    def states(self) -> Dict[str, State]:
        return self._states

    @property
    def ax(self) -> plt.Axes:
        if self._ax is None:
            self._ax = plt.gcf().add_subplot(1, 1, 1,
                                             projection=ccrs.PlateCarree())
        return self._ax

    @ax.setter
    def ax(self, axes):
        self._ax = axes

    @property
    def df(self) -> geopandas.GeoDataFrame:
        if self._df is None:
            self.generate_data()
        return self._df

    def _draw_empty(self, df: geopandas.GeoDataFrame):
        pass

    def _adjust_jk(self, df: geopandas.GeoDataFrame):
        # If lot of factors are different in this section, you should just
        # put override_jk as False and adjust it yourself by replacing
        # geometry in the DataFrame
        if not self.override_jk:
            return
        if not os.path.isfile(self.jk_file):
            warnings.warn("Shape files for Jammu and Kashmir disputed "
                          "region not found. Skipping the correction.")
            return

        if self.level != 1:
            warnings.warn("Jammu and Kashmir correction can be only applied "
                          "to level 1 admin map. In current case, you have "
                          "to do it by yourself.")
            return
        jk = geopandas.read_file(self.jk_file)
        gm = jk.loc[
            jk["st_nm"] == "Jammu & Kashmir",
            [self.COL_GEOMETRY]].values[0]

        df.loc[df[self.COL_STATE] == "Jammu and Kashmir", [
            self.COL_GEOMETRY]] = gm

    def generate_data(self):
        df = geopandas.read_file(self.filename)
        self._adjust_jk(df)
        df[self.COL_COLOR] = palette.ultramarine(shade=40)
        self._df = df

    def generate_states(self, meta=None):
        tmp = []
        for _, row in self.df.iterrows():
            s = State(row[self.COL_STATE], meta)
            s.geometry = row[self.COL_GEOMETRY]
            s.show_label = self.show_label
            tmp.append(s)
        self._states = {x.name: x for x in tmp if x.is_valid}
        return self.states

    def show(self):
        self.draw()
        plt.show()

    def draw(self):
        if self._df is None:
            self.generate_data()

        if len(self.states) == 0:
            self._draw_empty(self.df)
            self.df.plot(color=self.df[self.COL_COLOR])
        else:
            for s in self.states.values():
                self.ax.add_geometries([s.geometry],
                                       fc=s.color,
                                       crs=ccrs.PlateCarree())
                self.ax.set_extent(self.extent,
                                   crs=ccrs.PlateCarree())
                if s.show_label:
                    self.ax.text(s.x, s.y, s.label,
                                 ha="center", va="center")

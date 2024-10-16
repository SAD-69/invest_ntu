import os
import numpy as np
import matplotlib.pyplot as plt
import rasterio

from rasterio.transform import from_bounds
from rasterio.features import rasterize
from geopandas import GeoDataFrame, read_file
from esda.moran import Moran, Moran_Local, Moran_BV, Moran_Local_BV
from splot.esda import plot_moran, plot_local_autocorrelation
from libpysal.weights import Queen, Rook, KNN, DistanceBand, lag_spatial
from typing import Literal, Union

WeightTypes = Literal['queen', 'rook', 'knn', 'distance']
WeightClasses = Union[Queen, Rook, KNN, DistanceBand]


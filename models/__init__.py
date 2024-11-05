import os
import numpy as np
import matplotlib.pyplot as plt
import rasterio

from rasterio.transform import from_bounds
from rasterio.features import rasterize
from geopandas import GeoDataFrame, read_file, read_parquet
from pandas import Series
from esda.moran import Moran, Moran_Local, Moran_BV, Moran_Local_BV
from splot.esda import plot_moran, plot_local_autocorrelation
from pysal.model.mgwr import gwr
from libpysal.weights import Queen, Rook, KNN, DistanceBand, lag_spatial
from scipy.stats import monte_carlo_test, norm, shapiro

from typing import Literal, Union
from sklearn.linear_model import LinearRegression, PoissonRegressor
from sklearn.metrics import r2_score

WeightTypes = Literal['queen', 'rook', 'knn', 'distance']
WeightClasses = Union[Queen, Rook, KNN, DistanceBand]


def read_geo(path: str, layer: str = None) -> GeoDataFrame:
    gdal_drivers = {
        'shp': lambda: read_file(path),
        'geojson': lambda: read_file(path),
        'parquet': lambda: read_parquet(path),
        'gpkg': lambda: read_file(path, layer=layer)
    }
    for k, v in gdal_drivers.items():
        if path.endswith(f'.{k}'):
            return v()
        
    raise ValueError("Unsupported file format. Please use a supported file extension (shp, geojson, parquet, gpkg).")

import os
import numpy as np
import rasterio

from rasterio.transform import from_bounds
from rasterio.features import rasterize
from geopandas import GeoDataFrame, read_file
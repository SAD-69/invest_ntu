import os
import logging
import sys

import natcap.invest.urban_cooling_model
import natcap.invest.utils

from geopandas import GeoDataFrame, GeoSeries, read_file

import rasterio
from rasterio.mask import mask


shapefile = r"C:\Users\NTU-USER\Documents\ntu\landlord\teste_miguel\uv\uv_dados_fix.shp"
image = r"C:\Users\NTU-USER\Documents\ntu\landlord\teste_miguel\_clip_test\clipped_kmeans.tif"


LOGGER = logging.getLogger(__name__)
root_logger = logging.getLogger()

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    fmt=natcap.invest.utils.LOG_FMT,
    datefmt='%m/%d/%Y %H:%M:%S ')
handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[handler])

def rasterio_clip(shapefile_path: str, raster_path: str):
    gdf: GeoDataFrame = read_file(shapefile_path)
    # shapes = [feature["geometry"] for feature in gdf]

    for _, row in gdf.iterrows():
        with rasterio.open(raster_path) as src:
            out_image, out_transform = mask(src, [row['geometry']], crop=True)
            out_meta = src.meta

        out_meta.update({"driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform})
        uv = int(row['uv'])
        
        temp_gdf: GeoDataFrame = gdf.loc[gdf['uv'] == row['uv']]
        temp_gdf.to_file(r'C:\Users\NTU-USER\Documents\ntu\landlord\teste_miguel\uv\uv_py\uv_{0}.shp'.format(uv))

        with rasterio.open(r"C:\Users\NTU-USER\Documents\ntu\landlord\teste_miguel\uv\uv_py\clipped_{0}.tif".format(uv), "w", **out_meta) as dest:
            dest.write(out_image)

        args = {
            'aoi_vector_path': f'C:\\Users\\NTU-USER\\Documents\\ntu\\landlord\\teste_miguel\\uv\\uv_py\\uv_{uv}.shp',
            'avg_rel_humidity': '',
            'biophysical_table_path': 'C:\\Users\\NTU-USER\\Documents\\ntu\\landlord\\teste_miguel\\bio_table_all.csv',
            'building_vector_path': '',
            'cc_method': 'factors',
            'cc_weight_albedo': '',
            'cc_weight_eti': '',
            'cc_weight_shade': '',
            'do_energy_valuation': False,
            'do_productivity_valuation': False,
            'energy_consumption_table_path': '',
            'green_area_cooling_distance': '1000',
            'lulc_raster_path': f'C:\\Users\\NTU-USER\\Documents\\ntu\\landlord\\teste_miguel\\uv\\uv_py\\clipped_{uv}.tif',
            'ref_eto_raster_path': 'C:\\Users\\NTU-USER\\Documents\\ntu\\simulator_testes\\simulator_V2\\hydro_et_al.tif',
            'results_suffix': f'uv_{uv}',
            't_air_average_radius': '2000',
            't_ref': '24',
            'uhi_max': '3.5',
            'workspace_dir': 'C:\\Users\\NTU-USER\\Documents\\ntu\\landlord\\teste_miguel\\uv\\uv_py',
        }
        natcap.invest.urban_cooling_model.execute(args)








        

rasterio_clip(shapefile, image)
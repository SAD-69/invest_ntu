import sys
import logging

import natcap.invest.urban_cooling_model
import natcap.invest.utils

from dataclasses import dataclass
from typing import Literal

CC_METHODS = Literal['factors', 'intensity']

LOGGER = logging.getLogger(__name__)
root_logger = logging.getLogger()

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(
    fmt=natcap.invest.utils.LOG_FMT,
    datefmt='%m/%d/%Y %H:%M:%S ')
handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[handler])


@dataclass
class HeatMitigation:
    """_summary_

    Returns:
        _type_: _description_
    """
    aoi_shp: str
    biophysical_csv: str
    lulc_raster: str
    evap_raster: str
    workspace_dir: str
    uhi_max: int | str
    temp_air_ref: int | str
    temp_air_average_radius: int | str
    green_area_cooling_dist: int | str
    suffix: str = None
    building_shp: str = None
    avg_rel_humidity: int | str = None
    cc_weight_albedo: int | str = None
    cc_weight_eti: int | str = None
    cc_weight_shade: int | str = None
    cc_method: CC_METHODS = 'factors'
    energy_valuation: bool = False
    energy_consump_csv: str = None
    productivity_valuation: bool = False

    @property
    def args(self) -> dict[str, str]:
        return {
            'aoi_vector_path': self.aoi_shp,
            'avg_rel_humidity': self.avg_rel_humidity,
            'biophysical_table_path': self.biophysical_csv,
            'building_vector_path': self.building_shp,
            'cc_method': self.cc_method,
            'cc_weight_albedo': self.cc_weight_albedo,
            'cc_weight_eti': self.cc_weight_eti,
            'cc_weight_shade': self.cc_weight_shade,
            'do_energy_valuation': self.energy_valuation,
            'do_productivity_valuation': self.productivity_valuation,
            'energy_consumption_table_path': self.energy_consump_csv,
            'green_area_cooling_distance': self.green_area_cooling_dist,
            'lulc_raster_path': self.lulc_raster,
            'ref_eto_raster_path': self.evap_raster,
            'results_suffix': self.suffix,
            't_air_average_radius': self.temp_air_average_radius,
            't_ref': self.temp_air_ref,
            'uhi_max': self.uhi_max,
            'workspace_dir': self.workspace_dir
        }
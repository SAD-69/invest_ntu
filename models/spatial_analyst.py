from models import *

plt.style.use('ggplot')

class SpatialAnalyst:
    def __init__(self, vector: str):
        self.gdf = read_file(vector)
        self._gcol = self._get_geom_col(self.gdf)
        self._w_cache = {}

    def univariate_moran(self, col: str, weight_type: WeightTypes) -> tuple[Moran, Moran_Local]:
        w = self._select_weight(weight_type)
        w.transform = 'r'
        value = self.gdf[col]
        self.gdf['lag'] = lag_spatial(w, value)
        moran = Moran(self.gdf['lag'], w)
        lisa = Moran_Local(self.gdf['lag'], w)
        return moran, lisa
    
    def bivariate_moran(self, dep_col: str, ind_col: str, weight_type: WeightTypes):
        w = self._select_weight(weight_type)
        print(type(w))
        w.transform = 'r'
        dep_var = self.gdf[dep_col]
        ind_var = self.gdf[ind_col]
        
        self.gdf['lag'] = lag_spatial(w, dep_var)
        moran = Moran_BV(self.gdf['lag'], ind_var, w)
        lisa = Moran_Local_BV(self.gdf['lag'], ind_var, w)
        return moran, lisa
    
    def _select_weight(self, weight_type: WeightTypes) -> WeightClasses:
        if weight_type not in self._w_cache:
            weight_dict = {
                'queen': lambda: Queen.from_dataframe(self.gdf, geom_col=self._gcol),
                'rook': lambda: Rook.from_dataframe(self.gdf, geom_col=self._gcol),
                'knn': lambda: KNN.from_dataframe(self.gdf, geom_col=self._gcol, k=5),
                'distance': lambda: DistanceBand.from_dataframe(self.gdf, geom_col=self._gcol, threshold=1000)
            }
            self._w_cache[weight_type] = weight_dict.get(weight_type)()
        return self._w_cache[weight_type]
    
    def plot_analysis(self, moran: Union[Moran, Moran_BV, Moran_Local, Moran_Local_BV], attribute: str = None):
        if isinstance(moran, (Moran_Local, Moran_Local_BV)):
            plot_local_autocorrelation(moran, self.gdf, attribute)
        else:
            plot_moran(moran)
        return plt.show()
    
    @staticmethod
    def _get_geom_col(gdf: GeoDataFrame) -> str:
        return gdf.geometry.name
        # return [col for col in gdf.columns if 'geom' in col][0]
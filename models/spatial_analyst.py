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
    
    def linear_regression(self, ind_var: str, dep_var: str) -> float:
        X = self.gdf[[ind_var]]
        y = self.gdf[dep_var]
        lin_model = LinearRegression().fit(X, y)
        pred = lin_model.predict(X)
        score = r2_score(y_true=y, y_pred=pred)
        slope = lin_model.coef_[0]
        intercept = lin_model.intercept_

        plt.figure(figsize=(8, 6))
        plt.scatter(self.gdf[ind_var], self.gdf[dep_var], color='blue', label=ind_var, s=50)
        plt.plot(self.gdf[ind_var], pred, color='red', label='regression', linewidth=0.8)
        plt.xlabel(ind_var)
        plt.ylabel(dep_var)
        plt.title(f'Linear Regression Model (R^2 = {score:.3f})')
        plt.legend()
        plt.show()
        return score, slope, intercept
    
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
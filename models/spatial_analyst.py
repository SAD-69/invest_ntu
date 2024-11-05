from models import *
import statsmodels.api as sm

plt.style.use('seaborn-v0_8')


class SpatialAnalyst:
    def __init__(self, vector: str, layer: str = None):
        self.gdf = read_geo(vector, layer)
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
    
    def linear_regression(self, ind_var: str, dep_var: str, linear: bool = True) -> tuple[float, float, float]:
        """Gera regressão linear entre 2 colunas do GeoDataFrame

        Args:
            ind_var (str): Variável independente (X)
            dep_var (str): Variável dependente (y)
            linear (bool): Regressão linear (True) ou de poisson (False). Defaults to True

        Returns:
            score, slope e intercept (float) : Valor de correlação, declividade e intercepção
        """
        X = self.gdf[[ind_var]]
        y = self.gdf[dep_var]
        if linear:
            lin_model = LinearRegression().fit(X, y)
        else:
            lin_model = PoissonRegressor().fit(X, y)
        pred = lin_model.predict(X)
        score = r2_score(y_true=y, y_pred=pred)
        slope: float = lin_model.coef_[0]
        intercept = lin_model.intercept_

        X_constant = sm.add_constant(X)
        sm_model = sm.OLS(y, X_constant).fit()
        p_value = sm_model.pvalues[1]

        plt.figure(figsize=(8, 6))
        plt.scatter(self.gdf[ind_var], self.gdf[dep_var], color='blue', label=ind_var, s=50)
        plt.plot(self.gdf[ind_var], pred, color='red', label='regression', linewidth=0.8)
        plt.xlabel(ind_var)
        plt.ylabel(dep_var)
        plt.title(f'Linear Regression Model (R^2 = {score:.2f}, Slope = {slope:.3f}), p-value = {p_value:.3f}')
        plt.legend()
        plt.show()
        return score, slope, intercept, p_value
    
    def _shapiro_test(self, col: str) -> float:
        return shapiro(col).statistic
    
    def monte_carlo_plot(self, col: str) -> None:
        _, ax = plt.subplots(figsize=(8, 5))
        length = len(self.gdf)
        ref = monte_carlo_test(self.gdf[col], norm.rvs, self._shapiro_test, alternative='less')
        null_dist = ref.null_distribution
        bins = np.linspace(min(null_dist), 1, length + 10)
        ax.hist(ref.null_distribution, density=True, bins=bins)
        ax.set_title('Shapiro-Wilk Test Null Distribution \n'
                    f'(Monte Carlo Approximation, {length} Observations)')
        ax.set_xlabel('statistic')
        ax.set_ylabel('probability_denisty')
        annotation = (f'p-value={ref.pvalue:.6f}\n (highlighted area)')
        props = {'facecolor': 'black', 'width': 1, 'headwidth': 5, 'headlength': 8}
        i_ext = np.where(bins <= ref.statistic)[0]
        for i in i_ext:
            ax.patches[i].set_color('C1')

        if i_ext.size > 0:
            # Midpoint of the highlighted area for the x-coordinate
            x_annotate = (bins[i_ext[0]] + bins[i_ext[-1]]) / 2
            # Slightly above the tallest highlighted bin for the y-coordinate
            max_density = max(p.get_height() for i, p in enumerate(ax.patches) if i in i_ext)
            y_annotate = max_density + 0.05 * max_density  # Add some padding above the tallest bar

            # Set arrow properties
            props = {'facecolor': 'black', 'width': 1, 'headwidth': 5, 'headlength': 8}
            ax.annotate(annotation, xy=(x_annotate, y_annotate), 
                        xytext=(x_annotate, y_annotate + 0.1 * max_density), 
                        arrowprops=props, ha='center')

        plt.xlim(min(null_dist), max(null_dist))
        plt.ylim(0, ax.get_ylim()[1])
        plt.show()
    
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
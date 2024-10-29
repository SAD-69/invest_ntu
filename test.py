from models.spatial_analyst import SpatialAnalyst, plt, read_file
from scipy.stats import shapiro, anderson, kstest, skew, kurtosis
import statsmodels.api as sm
import matplotlib.pyplot as plt

path = r"C:\Users\NTU-USER\Downloads\isla_calor\isla_calor\hmi_cc_tmp_uv.geojson"
sa = SpatialAnalyst(path)
sa.shapiro_plot('avg_tmp_an')
# moran, lisa = sa.bivariate_moran('avg_cc', 'hm_mean', 'queen')
# print(sa.linear_regression('avg_cc', 'avg_tmp_an'))
# plt.show()
# moran, lisa = sa.univariate_moran('avg_cc', 'queen')
# print(moran.I, moran.p_sim)
# sa.plot_analysis(lisa, 'avg_cc')
# sa.plot_analysis()

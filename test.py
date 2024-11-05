from models.spatial_analyst import SpatialAnalyst

# path = r"C:\Users\NTU-USER\Downloads\isla_calor\isla_calor\hmi_cc_tmp_uv.geojson"
path = 'uv_dados_pol.parquet'
sa = SpatialAnalyst(path)
# sa.monte_carlo_plot('hmi_cc_diff')
moran, lisa = sa.bivariate_moran('ndvi_norm', 'hqi_norm', 'queen')
print(sa.linear_regression('ndvi_norm', 'hqi_norm'))
# print(sa.poisson_regression('Area (m2)', 'hmi_cc_diff'))
# plt.show()
# moran, lisa = sa.univariate_moran('hmi_cc_diff', 'knn')
print(moran.I, moran.p_sim)
sa.plot_analysis(lisa, 'ndvi_norm')
# sa.plot_analysis()

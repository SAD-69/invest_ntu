from models.spatial_analyst import SpatialAnalyst

# path = r"C:\Users\NTU-USER\Downloads\isla_calor\isla_calor\hmi_cc_tmp_uv.geojson"
path = 'moran_lotes_uv_2.geojson'
sa = SpatialAnalyst(path)
# sa.monte_carlo_plot('hmi_cc_diff')
moran, lisa = sa.bivariate_moran('Area (m2)', 'hmi_cc_diff', 'knn')
# print(sa.linear_regression('Area (m2)', 'hmi_cc_diff'))
# print(sa.poisson_regression('Area (m2)', 'hmi_cc_diff'))
# plt.show()
# moran, lisa = sa.univariate_moran('hmi_cc_diff', 'knn')
print(moran.I, moran.p_sim)
sa.plot_analysis(lisa, 'hmi_cc_diff')
# sa.plot_analysis()

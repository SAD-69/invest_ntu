from models.spatial_analyst import SpatialAnalyst, plt


sa = SpatialAnalyst('moran_lotes_uv_2.geojson')
# moran, lisa = sa.bivariate_moran('cc_mean', 'hmi_mean', 'knn')
print(sa.linear_regression('hmi_mean', 'cc_mean'))
plt.show()
# moran, lisa = sa.univariate_moran('hmi_mean', 'knn')
# print(moran.I)
# sa.plot_analysis(lisa, 'hmi_mean')
# sa.plot_analysis()

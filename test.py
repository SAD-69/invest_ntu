from models.spatial_analyst import SpatialAnalyst

sa = SpatialAnalyst('moran_lotes_uv_2.geojson')
# moran, lisa = sa.bivariate_moran('cc_mean', 'hmi_mean', 'knn')
moran, lisa = sa.univariate_moran('cc_mean', 'knn')
sa.plot_analysis(lisa, 'cc_mean')
sa.plot_analysis()

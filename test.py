from models.spatial_analyst import SpatialAnalyst, plt


sa = SpatialAnalyst(r"C:\Users\NTU-USER\Downloads\isla_calor\isla_calor\hmi_cc_tmp_uv.geojson")
moran, lisa = sa.bivariate_moran('avg_cc', 'hm_mean', 'queen')
# print(sa.linear_regression('avg_cc', 'avg_tmp_an'))
# plt.show()
# moran, lisa = sa.univariate_moran('avg_cc', 'queen')
print(moran.I, moran.p_sim)
sa.plot_analysis(lisa, 'avg_cc')
# sa.plot_analysis()

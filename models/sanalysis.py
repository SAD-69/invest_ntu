import matplotlib.pyplot as plt
from esda.moran import Moran, Moran_Local
from libpysal.weights import Queen, Rook, KNN, DistanceBand, lag_spatial
from geopandas import GeoDataFrame, read_file
from splot.esda import plot_moran, plot_local_autocorrelation

plt.style.use('fast')

path = r'C:/Users/NTU-USER/Documents/ntu/landlord/teste_miguel/uv/uv_py/uv_2_concept.gpkg'
gdf: GeoDataFrame = read_file(path, layer='lotes_cc_hmi_median')

w = KNN.from_dataframe(gdf, geom_col='geometry', k=5)
# w = Rook.from_dataframe(gdf, geom_col='geometry')
# w = Queen.from_dataframe(gdf, geom_col='geometry')
# w = DistanceBand.from_dataframe(gdf, geom_col='geometry', threshold=1000)
w.transform = 'R'
median_val = gdf['cc_median']
mean_val = gdf['cc_mean']

gdf['lag_median'] = lag_spatial(w, median_val)
gdf['lag_mean'] = lag_spatial(w, mean_val)

moran = Moran(gdf['lag_median'], w)
lisa = Moran_Local(gdf['lag_median'], w)
print('Median values Global Moran: ', moran.I)
print('p-value median: ', moran.p_sim)
# print(lisa.Is)

moran_mean = Moran(gdf['lag_mean'], w)
lisa_mean = Moran_Local(gdf['lag_mean'], w)
print('Mean values Global Moran: ', moran_mean.I)
print('p-value mean: ', moran_mean.p_sim)
# print(lisa_mean.Is)

# # plot_moran(moran)
# plot_local_autocorrelation(lisa, gdf, 'cc_median')

# # plot_moran(moran_mean)
# plot_local_autocorrelation(lisa_mean, gdf, 'cc_mean')
# plt.show()

gdf['local_moran_median'] = lisa.Is
gdf['local_moran_mean'] = lisa_mean.Is
gdf['p_values_median'] = lisa.p_sim
gdf['p_values_mean'] = lisa_mean.p_sim
gdf['z_scores_median'] = lisa.z_sim
gdf['z_scores_mean'] = lisa_mean.z_sim
gdf['significance_median'] = lisa.p_sim < 0.05
gdf['significance_mean'] = lisa_mean.p_sim < 0.05

gdf.to_file('moran_lotes_uv_2.geojson')

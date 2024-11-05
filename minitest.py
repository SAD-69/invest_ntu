import rasterio
import numpy as np
from scipy.stats import linregress
from rasterio.enums import Resampling
import matplotlib.pyplot as plt


def align_rasters(src_path1, src_path2, resampling=Resampling.nearest):
    # Open both rasters
    with rasterio.open(src_path1) as src1, rasterio.open(src_path2) as src2:
        # Get metadata of raster 1 to use as reference
        transform, width, height = src1.transform, src1.width, src1.height

        # Reproject raster 2 to match raster 1
        data1 = src1.read(1, masked=True)  # Masked array from raster 1
        data2 = src2.read(1, out_shape=(height, width), resampling=resampling, masked=True)  # Resample and mask
        
    return data1, data2

data1, data2 = align_rasters(
    r"C:\Users\NTU-USER\Documents\ntu\simulator_testes\simulator_V2\hmi_bbox.tif",
    # r"c:\Users\NTU-USER\Downloads\isla_calor\isla_calor\hm_uv_37_energy_savings_vias_verdes_v2.tif"    
    r"C:\Users\NTU-USER\Documents\ntu\simulator_v1\lst_median_2023_bbox.tif"
    )


# Mask the arrays to remove nodata pixels from both rasters
common_mask = data1.mask | data2.mask
data1: np.ma.MaskedArray = np.ma.array(data1, mask=common_mask)
data2: np.ma.MaskedArray = np.ma.array(data2, mask=common_mask)

# Flatten and compress for regression analysis
data1 = data1.compressed()
data2 = data2.compressed()


# Run linear regression on the masked arrays
slope, intercept, r_value, p_value, std_err = linregress(data1, data2)

# Plotting the regression graph
plt.figure(figsize=(8, 6))
plt.scatter(data1, data2, alpha=0.3, label='Data points', color='blue', s=5)

# Plot the regression line
x_vals = np.array([data1.min(), data1.max()])
y_vals = intercept + slope * x_vals
plt.plot(x_vals, y_vals, color='red', linewidth=2, label=f'Regression line (y = {slope:.2f}x + {intercept:.2f})')

print(f"Slope: {slope}")
print(f"Intercept: {intercept}")
print(f"R-squared: {r_value**2}")
print(f"P-value: {p_value}")
print(f"Standard error: {std_err}")

predicted_raster = slope * data1 + intercept  # Predicted values for each cell

# Add labels and title
plt.xlabel("Raster 1 Values")
plt.ylabel("Raster 2 Values")
plt.title(f"Regression Analysis\nR-squared: {r_value**2:.3f}, p-value: {p_value:.3e}")
plt.legend()
plt.grid(True)
plt.show()

# # Use the metadata from the first raster
# with rasterio.open("predicted_raster.tif", "w", **src1.meta) as dst:
#     dst.write(predicted_raster, 1)

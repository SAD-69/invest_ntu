import rasterio
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from rasterio.enums import Resampling

def align_rasters(src_path1, src_path2, resampling=Resampling.nearest):
    # Open both rasters
    with rasterio.open(src_path1) as src1, rasterio.open(src_path2) as src2:
        # Get metadata of raster 1 to use as reference
        transform, width, height = src1.transform, src1.width, src1.height

        # Reproject raster 2 to match raster 1
        data1 = src1.read(1, masked=True)  # Masked array from raster 1
        data2 = src2.read(1, out_shape=(height, width), resampling=resampling, masked=True)  # Resample and mask
        
    return data1, data2

# Align rasters to have the same shape and mask
data1, data2 = align_rasters("cc_bbox.tif", "temp_superficial.tif")

# Mask the arrays to remove nodata pixels from both rasters
common_mask = data1.mask | data2.mask
data1 = np.ma.array(data1, mask=common_mask)
data2 = np.ma.array(data2, mask=common_mask)

# Flatten and compress for regression analysis
data1 = data1.compressed()
data2 = data2.compressed().astype(int)  # Convert to integer for Poisson regression

# Add constant to predictor variable for intercept in Poisson regression
X = sm.add_constant(data1)

# Perform Poisson regression
poisson_model = sm.GLM(data2, X, family=sm.families.Poisson()).fit()

# Get the regression coefficients
intercept = poisson_model.params[0]
slope = poisson_model.params[1]
p_value = poisson_model.pvalues[1]

# Calculate McFadden's pseudo R-squared
null_model = sm.GLM(data2, np.ones_like(data2), family=sm.families.Poisson()).fit()
pseudo_r_squared = 1 - poisson_model.llf / null_model.llf

# Predicted values
predicted_raster = poisson_model.predict(X)

# Plotting the regression graph
plt.figure(figsize=(8, 6))
plt.scatter(data1, data2, alpha=0.3, label='Data points', color='blue', s=5)

# Plot the Poisson regression line
x_vals = np.linspace(data1.min(), data1.max(), 100)
y_vals = poisson_model.predict(sm.add_constant(x_vals))
plt.plot(x_vals, y_vals, color='red', linewidth=2, label=f'Poisson Regression (y = {slope:.2f}x + {intercept:.2f})')

# Print results
print(f"Slope: {slope}")
print(f"Intercept: {intercept}")
print(f"Pseudo R-squared (McFadden): {pseudo_r_squared}")
print(f"P-value: {p_value}")

# Add labels and title
plt.xlabel("Raster 1 Values")
plt.ylabel("Raster 2 Values")
plt.title(f"Poisson Regression Analysis\nPseudo R-squared: {pseudo_r_squared:.3f}, p-value: {p_value:.3e}")
plt.legend()
plt.grid(True)
plt.show()

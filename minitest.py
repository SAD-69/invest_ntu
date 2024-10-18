import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Example DataFrame
data = {
    'X': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Y': [1.5, 2.3, 3.1, 4.0, 4.8, 5.6, 6.5, 7.3, 8.1, 9.0]
}

df = pd.DataFrame(data)

# Reshape the 'X' values for the model (required by sklearn)
X = df[['X']]  # Feature (independent variable) as 2D array
Y = df['Y']    # Target (dependent variable)

# Create and fit the model
model = LinearRegression()
model.fit(X, Y)

# Predict Y values using the linear regression model
Y_pred = model.predict(X)

# Plot the data points and the regression line
plt.scatter(df['X'], df['Y'], color='blue', label='Original data')  # Scatter plot of the data
plt.plot(df['X'], Y_pred, color='red', label='Linear regression')   # Linear regression line
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Linear Regression with sklearn')
plt.legend()
plt.show()

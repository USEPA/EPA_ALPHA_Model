from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import numpy as np

# Generate sample data with 4 independent variables and 1 dependent variable
X = np.random.rand(100, 4)
y = np.random.rand(100)

# Create polynomial features
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# Fit linear regression model
model = LinearRegression()
model.fit(X_poly, y)

# Get coefficients and intercept
coef = model.coef_
intercept = model.intercept_

# Get feature names
feat_names = poly.get_feature_names_out(['x1', 'x2', 'x3', 'x4'])

# Create equation string
equation = f"{intercept:.2f} + "
for i, name in enumerate(feat_names):
    equation += f"{coef[i]:.2f} {name} + "
equation = equation[:-3]  # Remove the last " + "

print(equation)

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import csv

# Load the CSV file using NumPy's genfromtxt function
data = np.genfromtxt('book1.csv', delimiter=',', skip_header=1)

# Extract the second column into a separate array
x1 = data[:, 0]
x2 = data[:, 1]
x3 = data[:, 2]
x4 = data[:, 3]
y = data[:, 4]

# Create the design matrix
X = np.column_stack((x1, x2, x3, x4))
poly = PolynomialFeatures(degree=3)
X_design = poly.fit_transform(X)

# Fit the linear regression model
model = LinearRegression()
model.fit(X_design, y)

# Print the model coefficients
intercept = model.intercept_
coeff = model.coef_

# Get feature names
feat_names = poly.get_feature_names_out(['RLHP20', 'RLHP60', 'HP_ETW', 'ETW'])

# Create equation string
equation = f"{intercept:.15f} + "
for i, name in enumerate(feat_names):
    feat_names[i] = feat_names[i].replace(" ", " * ")
    equation = equation + str(coeff[i]) + " * " + feat_names[i] + " + "
equation = equation[:-3]  # Remove the last " + "

print(equation)
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import csv

# Load the input CSV
data = np.genfromtxt('ttt_1.csv', delimiter=',', skip_header=1)

# Extract the data into arrays
x1 = data[:, 0]
x2 = data[:, 1]
x3 = data[:, 2]
x4 = data[:, 3]
y = data[:, 4]

# Define the RSE parameters
X = np.column_stack((x1, x2, x3, x4))
poly = PolynomialFeatures(degree=2)
X_design = poly.fit_transform(X)

# Solve the RSE
model = LinearRegression()
model.fit(X_design, y)

# Get the model coefficients
intercept = model.intercept_
coeff = model.coef_

# Get feature names
feat_names = poly.get_feature_names_out(['RLHP20', 'RLHP60', 'HP_ETW', 'ETW'])

# Generate RSE equation for export
equation = f"{intercept:.15f} + "
for i, name in enumerate(feat_names):
    feat_names[i] = feat_names[i].replace(" ", " * ")
    equation = equation + str(coeff[i]) + " * " + feat_names[i] + " + "
equation = equation[:-3]  # Remove the last " + "

# print(equation)

# Export equation to file
output_file = open("equation.txt", "w")
output_file.write(equation)
output_file.close()
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
poly = PolynomialFeatures(degree=2)
X_design = poly.fit_transform(X)

# Fit the linear regression model
model = LinearRegression()
model.fit(X_design, y)

# Print the model coefficients
intercept = model.intercept_
coeff = model.coef_
coeff1 = coeff[0]
print(coeff1)
print(model.intercept_)
print(model.coef_)

# data to be written to CSV file
coeff_name = np.array(['Intercept', 'x1', 'x2', 'x3', 'x4', 'x1^2', 'x1 x2', 'x1 x3', 'x1 x4', 'x2^2', 'x2 x3',
              'x2 x4', 'x3^2', 'x3 x4', 'x4^2'])

coeff_value = np.array([intercept, coeff[1], coeff[2], coeff[3], coeff[4], coeff[5], coeff[6], coeff[7], coeff[8],
               coeff[9], coeff[10], coeff[11], coeff[12], coeff[13], coeff[14]])

# data = [("John", 28), ("Alice", 32), ("Bob", 19)]
# data = (coeff_name, coeff_value)
data = np.column_stack((coeff_name, coeff_value))

# open CSV file for writing
with open("coeff.csv", "w", newline="") as file:
    # create CSV writer object
    writer = csv.writer(file)

    # write header row (optional)
    writer.writerow(["Coefficient", "Value"])

    # write data rows
    for row in data:
        writer.writerow(row)

# n = 1

# x1 = x1[n]
# x2 = x2[n]
# x3 = x3[n]
# x4 = x4[n]
# y = y[n]

# ['1', 'x1', 'x2', 'x3', 'x4', 'x1^2', 'x1 x2', 'x1 x3', 'x1 x4', 'x2^2', 'x2 x3', 'x2 x4', 'x3^2', 'x3 x4', 'x4^2']


# row = intercept + coeff[0] \
#     + coeff[1]*x1 + coeff[2]*x2  + coeff[3]*x3 + coeff[4]*x4 \
#     + coeff[5]*x1*x1 + coeff[6]*x1*x2 + coeff[7]*x1*x3 + coeff[8]*x1*x4 \
#     + coeff[9]*x2*x2 + coeff[10]*x2*x3 + coeff[11]*x2*x4 \
#     + coeff[12]*x3*x3 + coeff[13]*x3*x4 + coeff[14]*x4*x4

# print(row, x1,x2,x3,x4,y)


# print(f'Response surface equation: {intercept:.2f} + {coeff[0]:.2f}x1 + {coeff[1]:.2f}x2 + {coeff[2]:.2f}x3\
# + {coeff[3]:.2f}x4 + {coeff[4]:.2f}x1^2 + {coeff[5]:.2f}x2^2 + {coeff[6]:.2f}x3^2 + {coeff[7]:.2f}x4^2\
#   + {coeff[8]:.2f}x1*X2 + {coeff[9]:.2f}x1*x3 + {coeff[10]:.2f}x1*x3 + {coeff[11]:.2f}x1*x4\
#    + {coeff[12]:.2f}x2*x3 + {coeff[13]:.2f}x2*x4 + {coeff[14]:.2f}x3*x4')



# l = model.predict(X_design)
# print(l)

# Add the array as a second column to the data array
# data = np.column_stack((data, l))

# Save the updated data array to the CSV file
# np.savetxt('data.csv', data, delimiter=',', fmt='%.8f')


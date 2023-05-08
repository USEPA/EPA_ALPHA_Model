import numpy as np
from scipy.optimize import curve_fit

# Define the function that generates the data
def func(x1, x2):
    return 3 + 2*x1 + 4*x2 + 3*x1*x2

# Define the range for each variable
x1_range = [-1, 1]
x2_range = [-1, 1]

x1 = np.array([1, 1, 1, 1, 1,1,1,1,1])
x2 = np.array([2, 2, 2, 2, 2,2,2,2,2])
y = np.array([3, 3, 3, 3, 3,3,3,3,3])

# Define the levels for the design
alpha = 1  # distance from the center to each vertex of the hypercube
star = 1.68  # distance from the center to each star point
n = 5  # number of levels for each variable (excluding center points)

# Generate the design matrix
x1c, x2c = np.meshgrid([-alpha, 0, alpha], [-alpha, 0, alpha])
x1s, x2s = np.meshgrid([-star, 0, star], [-star, 0, star])
X = np.column_stack([x1, x2, x1s.ravel(), x2s.ravel()])

# Generate the response vector
# y = func(*X.T)

# Fit a quadratic response surface model
def quad_func(X, a, b, c, d, e, f):
    x1, x2, x1s, x2s = X.T
    return a + b*x1 + c*x2 + d*x1**2 + e*x2**2 + f*x1*x2

popt, pcov = curve_fit(quad_func, X, y)

# Print the coefficients of the response surface equation
print(f'Response surface equation: {popt[0]:.2f} + {popt[1]:.2f}x1 + {popt[2]:.2f}x2 + {popt[3]:.2f}x1^2 + {popt[4]:.2f}x2^2 + {popt[5]:.2f}x1*x2')
print(popt)
print(pcov)

exit()



x1 = np.array([1, 1, 1, 1, 1])
x2 = np.array([2, 2, 2, 2, 2])
y = np.array([3, 3, 3, 3, 3])

# Generate the design matrix
X = np.column_stack([x1, x2, x1s.ravel(), x2s.ravel()])

# Fit a quadratic response surface model
popt, pcov = curve_fit(quad_func, X, y)

# Print the coefficients of the response surface equation
print(f'Response surface equation: {popt[0]:.2f} + {popt[1]:.2f}x1 + {popt[2]:.2f}x2 + {popt[3]:.2f}x1^2 + {popt[4]:.2f}x2^2 + {popt[5]:.2f}x1*x2')

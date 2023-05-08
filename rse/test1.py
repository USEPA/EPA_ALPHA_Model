import numpy as np
from scipy.optimize import curve_fit

# Define the function that generates the data
def func(x1, x2, x3, x4):
    return 5 + 2*x1 + 3*x2 + 4*x3 + 5*x4 + 3*x1*x2 + 2*x1*x3 + 2*x2*x3 + 4*x2*x4 + 5*x3*x4 + 2*x1**2 + 3*x2**2 + 4*x3**2 + 5*x4**2

# Define the range for each variable
x1_range = [-1, 1]
x2_range = [-1, 1]
x3_range = [-1, 1]
x4_range = [-1, 1]

x1 = np.array([1, 1, 1, 1, 1])
x2 = np.array([2, 2, 2, 2, 2])
x3 = np.array([3,3,3,3,3])
x4 = np.array([4,4,4,4,4])
y = np.array([5,5,5,5,5])

# Define the levels for the design
alpha = 1  # distance from the center to each vertex of the hypercube
star = 1  # distance from the center to each star point
n = 4  # number of levels for each variable (excluding center points)

# Generate the design matrix
x1c, x2c, x3c, x4c = np.meshgrid([-alpha, 0, alpha], [-alpha, 0, alpha], [-alpha, 0, alpha], [-alpha, 0, alpha])
x1s, x2s, x3s, x4s = np.meshgrid([-star, 0, star], [-star, 0, star], [-star, 0, star], [-star, 0, star])
X = np.column_stack([x1, x2, x3, x4])  #x1s.ravel(), x2s.ravel(), x3s.ravel(), x4s.ravel()])

# Generate the response vector
# y = func(*X.T)

# Fit a quadratic response surface model
def quad_func(X, a, b, c, d, e, f, g, h, i, j, k, l, m, n, o):
    x1, x2, x3, x4, = X.T
    return a + b*x1 + c*x2 + d*x3 + e*x4 + f*x1**2 + g*x2**2 + h*x3**2 + i*x4**2 + j*x1*x2 + k*x1*x3 + l*x1*x4 + m*x2*x3 + n*x2*x4 + o*x3*x4

popt, pcov = curve_fit(quad_func, X, y)

# Print the coefficients of the response surface equation
print(f'Response surface equation: {popt[0]:.2f} + {popt[1]:.2f}x1 + {popt[2]:.2f}x2 + {popt[3]:.2f}x3\
 + {popt[4]:.2f}x4 + {popt[5]:.2f}x1^2 + {popt[6]:.2f}x2^2 + {popt[7]:.2f}x3^2 + {popt[8]:.2f}x4^2\
    + {popt[9]:.2f}x1*X2 + {popt[10]:.2f}x1*x3 + {popt[11]:.2f}x1*x3 + {popt[12]:.2f}x1*x4\
    + {popt[13]:.2f}x2*x3 + {popt[14]:.2f}x2*x4 + {popt[15]:.2f}x3*x4')

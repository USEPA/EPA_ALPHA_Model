import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def iterate1(x1,x2,x3,x4,y,input1,input2,input3,input4,inputy):
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
    feat_names = poly.get_feature_names_out([input1, input2, input3, input4])

    # Generate RSE equation for export
    equation = f"{intercept:.15f} + "
    for i, name in enumerate(feat_names):
        feat_names[i] = feat_names[i].replace(" ", " * ")
        equation = equation + str(coeff[i]) + " * " + feat_names[i] + " + "
    equation = equation[:-3]  # Remove the last " + "
    equ = "(" + equation + ")"

    # Get the RSE predictions
    rse = model.predict(X_design)

    return equ, rse


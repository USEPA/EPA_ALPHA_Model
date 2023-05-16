import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import openpyxl

def iterate1(x1, y, x_values):
    # Define the RSE parameters
    X = np.column_stack((x1))
    poly = PolynomialFeatures(degree=2)
    X_design = poly.fit_transform(X)

    # Solve the RSE
    model = LinearRegression()
    model.fit(X_design, y)

    # Get the model coefficients
    intercept = model.intercept_
    coeff = model.coef_

    # Get feature names
    feat_names = poly.get_feature_names_out(x_values)

    # Generate RSE equation for export
    equation = f"{intercept:.15f} + "
    for i, name in enumerate(feat_names):
        feat_names[i] = feat_names[i].replace(" ", " * ")
        equation = equation + str(coeff[i]) + " * " + feat_names[i] + " + "
    equation = equation[:-3]  # Remove the last " + "
    equ = "(" + equation + ")"

    equ1 = equ
    while equ1.find('^') != -1:
        loc = equ1.find('^')
        d = equ1.rfind(" ",0,loc)
        e = equ1.find(" ", d+1)
        r = equ1[d+1:e]
        r1 = equ1[d+1:e-2]
        equ1 = equ1.replace(r, r1 + " * " + r1)

    print(equ)
    print(equ1)


    # Get the RSE predictions
    rse = model.predict(X_design)

    equ2 = equ1
    count = 0
    for b in x_values:
        equ2 = equ2.replace(x_values[count], str(X[0,count]))
        count += 1

    print(equ2)
    e = eval(equ2)
    print(e)
    print(rse[0])

    return equ1, rse


def read_column(filename, sheetname, column_name):
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook[sheetname]
    column_values = []

    column_index = None
    for cell in sheet[1]:  # Iterate through the first row to find the column index
        if cell.value == column_name:
            column_index = cell.column
            break

    if column_index is not None:
        for i, row in enumerate(sheet.iter_rows(values_only=True), start=1):
            if i > 1:  # Skip the first row
                cell_value = row[column_index - 1]
                if cell_value is not None:  # Ignore blank cells
                    column_values.append(cell_value)

    workbook.close()
    return column_values




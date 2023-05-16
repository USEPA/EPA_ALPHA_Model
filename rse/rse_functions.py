import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import openpyxl

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


# Usage example
#filename = 'example.xlsx'  # Replace with your file path
#sheetname = 'Sheet1'  # Replace with your sheet name
#column_index = 1  # Replace with the column index you want to read (1 for column A, 2 for column B, etc.)

#column_data = read_column(filename, sheetname, column_index)
#print(column_data)


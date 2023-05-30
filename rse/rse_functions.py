import sys
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import openpyxl
import tkinter as tk
from PIL import Image, ImageTk


def iterate1(x1, y, x_values):
    # Define the RSE parameters
    x = np.column_stack(x1)
    poly = PolynomialFeatures(degree=2)
    x_design = poly.fit_transform(x)

    # Solve the RSE
    model = LinearRegression()
    model.fit(x_design, y)

    # Get the model coefficients
    intercept = model.intercept_
    coeff = model.coef_

    # Get feature names from RSE solution
    feat_names = poly.get_feature_names_out(x_values)

    # Generate RSE equation for export
    equation = f"{intercept:.15f} + "
    for i, name in enumerate(feat_names):
        feat_names[i] = feat_names[i].replace(" ", " * ")
        equation = equation + str(coeff[i]) + " * " + feat_names[i] + " + "
    equation = equation[:-3]  # Remove the last " + "
    equ = "( " + equation + " )"

    # Replace equation terms with '^' as this is not valid in Python.
    equ1 = equ
    while equ1.find('^') != -1:
        loc = equ1.find('^')
        d = equ1.rfind(" ", 0, loc)
        e = equ1.find(" ", d+1)
        r = equ1[d+1:e]
        r1 = equ1[d+1:e-2]
        r2 = equ1[loc+1:e]
        r3 = int(r2)
        str1 = r1
        # Add number of multiply terms based on power
        for _ in range(r3-1):
            str1 += " * " + r1
        # Replace '^' terms in equation with solution
        equ1 = equ1.replace(r, str1)

    # Get the RSE predictions
    rse = model.predict(x_design)

    # Insert actual values into equation to check equation syntax accuracy
    equ2 = equ1
    count = 0
    for _ in x_values:
        equ2 = equ2.replace(" " + x_values[count] + " ", " " + str(x[0, count]) + " ")
        count += 1

    e = eval(equ2)
    f = rse[0]
    g = (e-f)/ (e + sys.float_info.epsilon)
    if abs(g) > 0.0001:
        print(equ1)
        print("Formula Error")
        exit()

    if 'CO2' in y.name:
        equ1 = 'max(0, %s)' % equ1
        rse = np.maximum(0, rse)

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


def resize_image(image, max_width, max_height):
    width, height = image.size
    aspect_ratio = width / height

    if width > max_width or height > max_height:
        if width > height:
            new_width = max_width
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = max_height
            new_width = int(new_height * aspect_ratio)

        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        return resized_image
    else:
        return image


def create_image_window(window, image_files, grid_columns, max_width, max_height):
    # window = tk.Tk()
    window.title("ALPHA vs RSE Check Plots")

    # total_images = len(image_files)
    # grid_rows = (total_images + grid_columns - 1) // grid_columns

    for i, file in enumerate(image_files):
        image = Image.open(file)
        resized_image = resize_image(image, max_width, max_height)
        photo = ImageTk.PhotoImage(resized_image)
        label = tk.Label(window, image=photo)
        label.image = photo  # Keep a reference to the image to prevent garbage collection
        label.grid(row=i // grid_columns, column=i % grid_columns, padx=10, pady=10)

    window.mainloop()

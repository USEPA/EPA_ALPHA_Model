import sys
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import openpyxl
from PIL import Image, ImageDraw, ImageFont
import math


def iterate1(x1, y, x_values):
    """

    Parameters
    ----------
    x1
    y
    x_values

    Returns
    -------

    """
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
    g = (e-f) / (e + sys.float_info.epsilon)
    if abs(g) > 0.0001:
        print(equ1)
        print("Formula Error")
        exit()

    if 'CO2' in y.name:
        equ1 = 'max(0, %s)' % equ1
        rse = np.maximum(0, rse)

    return equ1, rse


def combine_images(image_paths, output_path, input_filename):
    images = [Image.open(path) for path in image_paths]

    # Calculate the grid dimensions based on the total number of images and the desired grid size
    num_images = len(images)
    rows = math.ceil(math.sqrt(num_images))
    cols = math.ceil(num_images / rows)

    # Calculate the size of each grid cell
    cell_width = max(image.width for image in images)
    cell_height = max(image.height for image in images)

    # Calculate the size of the combined image
    combined_width = cols * cell_width
    combined_height = rows * cell_height

    # Create a new combined image with a white background
    combined_image = Image.new('RGB', (combined_width, combined_height), 'white')

    # Paste each image into the appropriate grid cell
    for i, image in enumerate(images):
        col = i % cols
        row = i // cols
        x = col * cell_width
        y = row * cell_height
        combined_image.paste(image, (x, y))

    # Add title to image
    image = combined_image
    space_height = 100
    font_size = 32
    title = ' ALPHA vs RSE for: ' + input_filename
    # Create a new image with additional space
    width, height = image.size
    new_height = height + space_height
    new_image = Image.new("RGB", (width, new_height), (255, 255, 255))

    # Paste the original image onto the new image
    new_image.paste(image, (0, space_height))

    # Get a drawing context
    draw = ImageDraw.Draw(new_image)

    # Load the font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.truetype("Arial.ttf", font_size)

    # Calculate the position to place the title
    title_width, title_height = draw.textbbox((0, 0), title, font=font)[:2]
    title_x = 0
    title_y = int((space_height - title_height) / 2)

    # Draw the black background for the title
    title_bg = Image.new("RGB", (width, space_height), (255, 255, 255))
    new_image.paste(title_bg, (0, 0))

    # Draw the title on the new image
    draw.text((title_x, title_y), title, font=font, fill=(0, 0, 0))

    # Save the result
    new_image.save(output_path)


import os
import shutil
import sys

from matplotlib import pyplot as plt
from rse_functions import *
import pandas as pd
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFileDialog

app = QApplication([])
while 1:
    # Open file dialog for ALPHA input file
    input_file, _ = QFileDialog.getOpenFileName(None, "Open ALPHA Results File", "",
                                                "CSV Files (*.csv);;All Files (*.*)")
    # Save the path of the selected input file
    file_path = os.path.dirname(input_file)
    # Create path to configuration file in the same directory as the input file
    config_path = os.path.join(file_path, "configuration.xlsx")

    # Exit if file error or user cancels dialog
    if not os.path.exists(input_file):
        sys.exit()

    # Read RSE input and output values from configuration file
    x_values = read_column(config_path, 'Sheet1', 'RSE Inputs')
    y_values = read_column(config_path, 'Sheet1', 'RSE Outputs')

    # Clear arrays
    equation = []
    out = []
    out1 = []
    x1 = []

    # Read the ALPHA file into dataframes
    # Save the original file for output later
    alpha_csv = pd.read_csv(input_file)
    # Read again skipping second row of units
    df = pd.read_csv(input_file, skiprows=[1])

    # Get input data columns from input file (x)
    count = 0
    for x in x_values:
        x1.append(df[x_values[count]])
        count += 1

    # Generate RSE equations iterating through all output values (y)
    count = 0
    for x in y_values:
        y = df[x]
        equ, rse = iterate1(x1, y, x_values)

        if count == 0:
            count1 = 0
            out = pd.DataFrame()
            for b in x_values:
                out.insert(count1, x_values[count1], x1[count1], True)
                count1 += 1

        # Add original and RSE output data to dataframe
        out1 = pd.DataFrame(out)
        out1[y_values[count] + "-ALPHA"] = y
        out1[y_values[count] + "-RSE"] = rse
        out = pd.DataFrame(out1)
        # Generate check plot
        out.plot(x=y_values[count] + "-ALPHA", y=y_values[count] + "-RSE", style='o', legend=None, color="black")
        # Add titles to plot
        font1 = {'family': 'arial', 'color': 'black', 'size': 20}
        font2 = {'family': 'arial', 'color': 'black', 'size': 15}
        plt.title(y_values[count], fontdict=font1)
        plt.xlabel(y_values[count] + "-ALPHA", fontdict=font2)
        plt.ylabel(y_values[count] + "-RSE", fontdict=font2)
        # Calculate equation for trend line
        z = np.polyfit(out[y_values[count] + "-ALPHA"], out[y_values[count] + "-RSE"], 1)
        p = np.poly1d(z)
        # Add trend line to plot
        plt.plot(out[y_values[count] + "-ALPHA"], p(out[y_values[count] + "-ALPHA"]), color="black")
        plt.savefig('plot' + str(count) + '.png')
        plt.close()
        # Add equation to array
        equation.append(equ)
        count += 1

    # Create dataframe of equations
    equation1 = pd.DataFrame({"Value": y_values, "Equation": equation})

    # Strip off .csv and add .xlsx to ALPHA filename
    filename = Path(input_file)
    filename = filename.with_suffix('')
    filename = filename.with_suffix('.xlsx')

    # Write out Excel workbook file with multiple worksheets
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    # Write Equation worksheet
    equation1.to_excel(writer, sheet_name='Equation')
    worksheet = writer.sheets['Equation']
    worksheet.autofit()
    # Write out Data worksheet
    out1.to_excel(writer, sheet_name='Data')
    worksheet = writer.sheets['Data']
    worksheet.autofit()
    # Write original ALPHA data
    alpha_csv.to_excel(writer, sheet_name='ALPHA_Input', index=False)
    worksheet = writer.sheets['ALPHA_Input']
    worksheet.autofit()
    # Write out check plots
    workbook = writer.book
    count = 0
    for x in y_values:
        workbook.add_worksheet('Plot ' + str(count))
        worksheet = writer.sheets['Plot ' + str(count)]
        plot_name = 'plot' + str(count) + '.png'
        worksheet.insert_image('A1', plot_name)
        count += 1
    writer.close()

    image_files = []
    # Load check plot files
    count = 0
    for x in y_values:
        plot_name = 'plot' + str(count) + '.png'
        image_files.append(plot_name)
        count += 1

    # Display check plots
    grid_columns = 4
    max_width = 300
    max_height = 300
    create_image_window(image_files, grid_columns, max_width, max_height)

    # Delete check plot files
    for x in image_files:
        if os.path.exists(x):
            os.remove(x)

    # Move completed input file
    new_directory = "Completed"
    # Get the current input file directory
    current_directory = file_path
    # Create subdirectory 'Completed' if it does not exist
    new_directory_path = os.path.join(current_directory, new_directory)
    # Check if the directory already exists
    if not os.path.exists(new_directory_path):
        # Create the new directory
        os.makedirs(new_directory_path)
    # Move completed input file to 'Completed' subdirectory
    shutil.move(input_file, new_directory_path)
# The main while loop continues

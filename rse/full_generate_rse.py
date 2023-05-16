import os

import pandas
from matplotlib import pyplot as plt
from rse_functions import *
import sys
import xlsxwriter
import pandas as pd
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QFileDialog

# Open file dialog for ALPHA input file
app = QApplication([])
input_file, _ = QFileDialog.getOpenFileName(None, "Open ALPHA Results File", "", "All Files (*.*);;CSV Files (*.csv)")

# Clear arrays
inputy = []
equation = []
plots = []
# Define the input variables to locate in the ALPHA file
input1 = "RLHP20"
input2 = "RLHP60"
input3 = "HP_ETW"
input4 = "ETW"
inputy.append("EPA_FTP_1 gCO2/mi")
inputy.append("EPA_FTP_2 gCO2/mi")
inputy.append("EPA_FTP_3 gCO2/mi")
inputy.append("EPA_HWFET gCO2/mi")
inputy.append("EPA_US06_1 gCO2/mi")
inputy.append("EPA_US06_2 gCO2/mi")
inputy.append("Engine Displacement L")
inputy.append("Engine Cylinders")

# Read the ALPHA file into dataframes
# Save the original file for output later
alpha_csv = pd.read_csv(input_file)
# Read again skipping second row of units
df=pd.read_csv(input_file, skiprows=[1])

# Get input data columns
x1 = df[input1]
x2 = df[input2]
x3 = df[input3]
x4 = df[input4]

# Generate RSE equations iterating through all y values
count = 0
for x in inputy:
    y = df[x]
    equ, rse = iterate1(x1,x2,x3,x4,y,input1,input2,input3,input4,inputy[count])
    if count == 0:
        out = pd.DataFrame({input1: x1, input2: x2, input3: x3, input4: x4})

    # Add original and RSE output data to dataframe
    out1 = pd.DataFrame(out)
    out1[inputy[count] + "-ALPHA"] = y
    out1[inputy[count] + "-RSE"] = rse
    out = pd.DataFrame(out1)
    # Generate check plot
    out.plot(x=inputy[count] + "-ALPHA", y=inputy[count] + "-RSE", style='o', legend=None, color="black")
    # Add titles to plot
    font1 = {'family': 'arial', 'color': 'black', 'size': 20}
    font2 = {'family': 'arial', 'color': 'black', 'size': 15}
    plt.title(inputy[count], fontdict=font1)
    plt.xlabel(inputy[count] + "-ALPHA", fontdict=font2)
    plt.ylabel(inputy[count] + "-RSE", fontdict=font2)
    # calculate equation for trendline
    z = np.polyfit(out[inputy[count] + "-ALPHA"], out[inputy[count] + "-RSE"], 1)
    p = np.poly1d(z)
    # add trendline to plot
    plt.plot(out[inputy[count] + "-ALPHA"], p(out[inputy[count] + "-ALPHA"]), color="black")
    plt.savefig('plot' + str(count) + '.png')

    # Add equation to array
    equation.append(equ)

    count += 1

# Show check plots
# plt.show()

# Create dataframe of equations
equation1 = pd.DataFrame({"Value" : inputy, "Equation" : equation})

#strip off .csv and add .xlsx to ALPHA filename
filename = Path(input_file)
filename = filename.with_suffix('')
filename = filename.with_suffix('.xlsx')

#Write out Excel workbook file with multiple worksheets
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
workbook  = writer.book
count = 0
# exit()
for x in inputy:
    workbook.add_worksheet('Plot ' + str(count))
    worksheet = writer.sheets['Plot ' + str(count)]
    plot_name = 'plot' + str(count) + '.png'
    worksheet.insert_image('A1', plot_name)
    count += 1

writer.close()

# Delete check plot files
count = 0
for x in inputy:
    plot_name = 'plot' + str(count) + '.png'
    if os.path.exists(plot_name):
        os.remove(plot_name)
    count += 1

# End script
sys.exit()


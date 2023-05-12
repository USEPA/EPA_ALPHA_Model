from matplotlib import pyplot as plt
from rse_functions import *
import os
# import xlsxwriter
import pandas as pd

inputy = []
equation = []
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

# Read the ALPHA file
df=pd.read_csv("2022_09_15_17_30_26_LMDV_CVM_car_GDI_TRX10_FWD_SS1_results.csv", skiprows=[1])

# Get input data columns
x1 = df[input1]
x2 = df[input2]
x3 = df[input3]
x4 = df[input4]

# Iterate through all y values
if os.path.exists("equation.txt"):
  os.remove("equation.txt")
count = 0
for x in inputy:
    y = df[x]
    equ, rse = iterate1(x1,x2,x3,x4,y,input1,input2,input3,input4,inputy[count])
    if count == 0:
        out = pd.DataFrame({input1: x1, input2: x2, input3: x3, input4: x4})

    # Add RSE output to dataframe
    out1 = pd.DataFrame(out)
    out1[inputy[count]] = y
    out1[inputy[count] + "-RSE"] = rse
    out = pd.DataFrame(out1)
    # Generate check plots
    out.plot(x=inputy[count], y=inputy[count] + "-RSE", style='o')
    equation.append(equ)

    count += 1

# Output completed results file
# out1.to_csv("data.csv", index=False)

# Show check plots
plt.show()

# Export equation to file
equation1 = pd.DataFrame({"Value" : inputy, "Equation" : equation})
# df.to_csv("equation.csv", index=False)

# equation1 = pd.DataFrame(equation)


writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
# df = pd.read_csv('equation.csv')
equation1.to_excel(writer, sheet_name='Equation')
# df = pd.read_csv('data.csv')
out1.to_excel(writer, sheet_name='Data')
writer.close()





import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from rse_functions import *
import csv

inputy = []
filename = []
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

filename.append("ftp1")
filename.append("ftp2")
filename.append("ftp3")
filename.append("hwfet")
filename.append("us06_1")
filename.append("us06_2")

# Read the ALPHA file
df=pd.read_csv("2022_09_15_17_30_26_LMDV_CVM_car_GDI_TRX10_FWD_SS1_results.csv", skiprows=[1])

# Get input data columns
x1 = df[input1]
x2 = df[input2]
x3 = df[input3]
x4 = df[input4]

count = 0
for x in inputy:
    y = df[x]
    iterate1(x1,x2,x3,x4,y,input1,input2,input3,input4,inputy[count],filename[count])
    count += 1

# Export equation to file
output_file = open("equation.txt", "w")
output_file.write(equation)
output_file.close()




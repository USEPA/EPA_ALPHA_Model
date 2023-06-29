import os
import tkinter as tk
from tkinter import filedialog as fd
from datetime import datetime
import pandas as pd

ice_header = 'input_template_name:,context.rse_cost_clouds,input_template_version:,0.22'
phev_header = 'input_template_name:,context.rse_cost_clouds,input_template_version:,0.22'
bev_header = 'input_template_name:,context.rse_cost_clouds,input_template_version:,0.13'

def get_filepathname(filename):
    """
    Returns file name without extension, including path, e.g. /somepath/somefile.txt -> /somepath/somefile

    :param filename: file name, including path to file as required
    :return: file name without extension, including path
    """
    return os.path.splitext(filename)[0]


def get_filename(filename):
    """
    Returns file name without extension, e.g. /somepath/somefile.txt -> somefile

    :param filename: file name, including path to file as required
    :return: file name without extension
    """
    return os.path.split(get_filepathname(filename))[1]


root = tk.Tk()
root.withdraw()

loop = True

while loop:

    input_files = fd.askopenfilenames(title="Open RSE Files", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))

    rse_dfs = []

    if input_files:
        for input_filepathname in input_files:
            input_filename = get_filename(input_filepathname)

            print('processing %s ...' % input_filename)

            file_path = os.path.dirname(input_filepathname)

            os.chdir(file_path)

            input_df = pd.read_csv(input_filepathname)

            rse_dfs.append(input_df)

        collated_rse = pd.concat(rse_dfs, ignore_index=True, sort=False)

        output_filename = 'simulated_vehicles_rse_%s_%s.csv' % \
                          (get_filename(file_path), datetime.now().strftime('%Y_%m_%d'))

        # write template header
        if 'BEV' in get_filename(file_path):
            template_header = pd.DataFrame([str.split(bev_header, ',')])
        elif 'PHEV' in get_filename(file_path):
            template_header = pd.DataFrame([str.split(phev_header, ',')])
        else:
            template_header = pd.DataFrame([str.split(ice_header, ',')])

        template_header.to_csv(output_filename, header=False, index=False)

        collated_rse.to_csv(output_filename, mode='a', header=True, index=False)

    else:
        loop = False

print('done')

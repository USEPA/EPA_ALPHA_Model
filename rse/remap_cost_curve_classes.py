import os
import tkinter as tk
from tkinter import filedialog as fd
import pandas as pd


ldv_cost_curve_map = {
    'GDI_TRX10_SS0': 'ICE_SLA_FWD_GDI_TRX10F_SS0',
    'TDS_TRX10_SS0': 'ICE_SLA_FWD_TDS_TRX10F_SS0',

    'TDS_TRX12_SS0': 'ICE_SLA_FWD_TDS_TRX12F_SS0',
    'TDS_TRX12_SS1': 'ICE_SLA_FWD_TDS_TRX12F_SS1',
    'GDI_TRX12_SS0': 'ICE_SLA_FWD_GDI_TRX12F_SS0',
    'GDI_TRX12_SS1': 'ICE_SLA_FWD_GDI_TRX12F_SS1',
    'GDI_DEAC_D_TRX12_SS0': 'ICE_SLA_FWD_GDI_DEAC_D_TRX12F_SS0',
    'GDI_DEAC_D_TRX12_SS1': 'ICE_SLA_FWD_GDI_DEAC_D_TRX12F_SS1',
    'MIL_TRX12_SS0': 'ICE_SLA_FWD_MILLER_TRX12F_SS0',
    'MIL_TRX12_SS1': 'ICE_SLA_FWD_MILLER_TRX12F_SS1',

    'TDS_TRX22_SS0': 'ICE_SLA_FWD_TDS_TRX22F_SS0',
    'TDS_TRX22_SS1': 'ICE_SLA_FWD_TDS_TRX22F_SS1',
    'GDI_TRX22_SS0': 'ICE_SLA_FWD_GDI_TRX22F_SS0',
    'GDI_TRX22_SS1': 'ICE_SLA_FWD_GDI_TRX22F_SS1',
    'GDI_DEAC_D_TRX22_SS0': 'ICE_SLA_FWD_GDI_DEAC_D_TRX22F_SS0',
    'GDI_DEAC_D_TRX22_SS1': 'ICE_SLA_FWD_GDI_DEAC_D_TRX22F_SS1',
    'MIL_TRX22_SS0': 'ICE_SLA_FWD_MILLER_TRX22F_SS0',
    'MIL_TRX22_SS1': 'ICE_SLA_FWD_MILLER_TRX22F_SS1',

    'FCV': 'FCV',

    'BEV': 'BEV',

    'PHEV': 'P2_PHEV_SLA_FWD_GDI_TRX12F_SS1_AER0',  # for now... we might need to add one for something like BMW i3 REX

    'PS_MIL_TRXCV': 'PS_SLA_FWD_MILLER_TRXECVTF_SS1_BAD_REMOVED',
    'PS_DHE_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',
    'PS_DHE2_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',  # WHAT'S A DHE2?  NO SUCH ENGINE IN THE RSE BATCH
}


mdv_cost_curve_map = {
    'MIL_TRX12_SS0': 'MDV_ICE_HLA_RWD_DIESEL_TRX10R_SS0',
    'GDI_TRX12_SS0': 'MDV_ICE_HLA_RWD_PFI_TRX10R_SS0',  # NO GDI OPTION IN MDV RSE BATCH ...
}


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

input_files = fd.askopenfilenames(title="Open Vehicles File", filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))

if input_files:
    for input_filepathname in input_files:
        input_filename = get_filename(input_filepathname)

        print('processing %s ...' % input_filename)

        file_path = os.path.dirname(input_filepathname)

        os.chdir(file_path)

        template_header = pd.read_csv(input_filepathname, header=None, nrows=1)

        vehicle_data_df = pd.read_csv(input_filepathname, skiprows=[0])

        print(vehicle_data_df['cost_curve_class'].unique())

        if 'mdv' in input_filename:  # MIGHT NEED A BETTER WAY TO DO THIS, BUT FOR NOW...
            cost_curve_map = mdv_cost_curve_map
        else:
            cost_curve_map = ldv_cost_curve_map

        vehicle_data_df.loc[:, 'cost_curve_class'].replace(cost_curve_map, inplace=True)

        output_filename = 'remapped_%s.csv' % input_filename

        print('saving %s ...' % output_filename)

        # write template header
        template_header.to_csv(output_filename, header=False, index=False)

        # write data
        vehicle_data_df.to_csv(output_filename, mode='a', header=True, index=False)

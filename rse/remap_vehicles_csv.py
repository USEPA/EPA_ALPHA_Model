import os
import tkinter as tk
from tkinter import filedialog as fd
import pandas as pd


ldv_map = dict()
mdv_map = dict()

ldv_map['cost_curve_class'] = {
    "(vehicle_data_df['drive_system'] == 1) & (vehicle_data_df['application_id'] == 'SLA')": {
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

        'BEV': 'BEV_FWD',

        'PHEV': 'P2_PHEV_SLA_FWD_GDI_TRX12F_SS1_AER0',  # for now... we might need to add one for something like BMW i3 REX

        'PS_MIL_TRXCV': 'PS_SLA_FWD_MILLER_TRXECVTF_SS1',
        'PS_DHE_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',
        'PS_DHE2_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',  # WHAT'S A DHE2?  NO SUCH ENGINE IN THE RSE BATCH
    },

    "(vehicle_data_df['drive_system'] == 2) & (vehicle_data_df['application_id'] == 'SLA')": {
        'GDI_TRX10_SS0': 'ICE_SLA_RWD_GDI_TRX10R_SS0',
        'TDS_TRX10_SS0': 'ICE_SLA_RWD_TDS_TRX10R_SS0',

        'TDS_TRX12_SS0': 'ICE_SLA_RWD_TDS_TRX12R_SS0',
        'TDS_TRX12_SS1': 'ICE_SLA_RWD_TDS_TRX12R_SS1',
        'GDI_TRX12_SS0': 'ICE_SLA_RWD_GDI_TRX12R_SS0',
        'GDI_TRX12_SS1': 'ICE_SLA_RWD_GDI_TRX12R_SS1',
        'GDI_DEAC_D_TRX12_SS0': 'ICE_SLA_RWD_GDI_DEAC_D_TRX12R_SS0',
        'GDI_DEAC_D_TRX12_SS1': 'ICE_SLA_RWD_GDI_DEAC_D_TRX12R_SS1',
        'MIL_TRX12_SS0': 'ICE_SLA_RWD_MILLER_TRX12R_SS0',
        'MIL_TRX12_SS1': 'ICE_SLA_RWD_MILLER_TRX12R_SS1',

        'TDS_TRX22_SS0': 'ICE_SLA_RWD_TDS_TRX22R_SS0',
        'TDS_TRX22_SS1': 'ICE_SLA_RWD_TDS_TRX22R_SS1',
        'GDI_TRX22_SS0': 'ICE_SLA_RWD_GDI_TRX22R_SS0',
        'GDI_TRX22_SS1': 'ICE_SLA_RWD_GDI_TRX22R_SS1',
        'GDI_DEAC_D_TRX22_SS0': 'ICE_SLA_RWD_GDI_DEAC_D_TRX22R_SS0',
        'GDI_DEAC_D_TRX22_SS1': 'ICE_SLA_RWD_GDI_DEAC_D_TRX22R_SS1',
        'MIL_TRX22_SS0': 'ICE_SLA_RWD_MILLER_TRX22R_SS0',
        'MIL_TRX22_SS1': 'ICE_SLA_RWD_MILLER_TRX22R_SS1',

        'FCV': 'FCV',

        'BEV': 'BEV_RWD',

        'PHEV': 'P2_PHEV_SLA_RWD_GDI_TRX12R_SS1_AER0',
        # for now... we might need to add one for something like BMW i3 REX

        # ONLY FWD PS SO FAR...
        'PS_MIL_TRXCV': 'PS_SLA_FWD_MILLER_TRXECVTF_SS1',
        'PS_DHE_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',
        'PS_DHE2_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',  # WHAT'S A DHE2?  NO SUCH ENGINE IN THE RSE BATCH
    },

    "(vehicle_data_df['drive_system'] == 4) & (vehicle_data_df['application_id'] == 'SLA')": {
        'GDI_TRX10_SS0': 'ICE_SLA_AWD_GDI_TRX10R_SS0',
        'TDS_TRX10_SS0': 'ICE_SLA_AWD_TDS_TRX10R_SS0',

        'TDS_TRX12_SS0': 'ICE_SLA_AWD_TDS_TRX12R_SS0',
        'TDS_TRX12_SS1': 'ICE_SLA_AWD_TDS_TRX12R_SS1',
        'GDI_TRX12_SS0': 'ICE_SLA_AWD_GDI_TRX12R_SS0',
        'GDI_TRX12_SS1': 'ICE_SLA_AWD_GDI_TRX12R_SS1',
        'GDI_DEAC_D_TRX12_SS0': 'ICE_SLA_AWD_GDI_DEAC_D_TRX12R_SS0',
        'GDI_DEAC_D_TRX12_SS1': 'ICE_SLA_AWD_GDI_DEAC_D_TRX12R_SS1',
        'MIL_TRX12_SS0': 'ICE_SLA_AWD_MILLER_TRX12R_SS0',
        'MIL_TRX12_SS1': 'ICE_SLA_AWD_MILLER_TRX12R_SS1',

        'TDS_TRX22_SS0': 'ICE_SLA_AWD_TDS_TRX22R_SS0',
        'TDS_TRX22_SS1': 'ICE_SLA_AWD_TDS_TRX22R_SS1',
        'GDI_TRX22_SS0': 'ICE_SLA_AWD_GDI_TRX22R_SS0',
        'GDI_TRX22_SS1': 'ICE_SLA_AWD_GDI_TRX22R_SS1',
        'GDI_DEAC_D_TRX22_SS0': 'ICE_SLA_AWD_GDI_DEAC_D_TRX22R_SS0',
        'GDI_DEAC_D_TRX22_SS1': 'ICE_SLA_AWD_GDI_DEAC_D_TRX22R_SS1',
        'MIL_TRX22_SS0': 'ICE_SLA_AWD_MILLER_TRX22R_SS0',
        'MIL_TRX22_SS1': 'ICE_SLA_AWD_MILLER_TRX22R_SS1',

        'FCV': 'FCV',

        'BEV': 'BEV_AWD',

        'PHEV': 'P2_PHEV_SLA_AWD_GDI_TRX12R_SS1_AER0',
        # for now... we might need to add one for something like BMW i3 REX

        # ONLY FWD PS SO FAR...
        'PS_MIL_TRXCV': 'PS_SLA_FWD_MILLER_TRXECVTF_SS1',
        'PS_DHE_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',
        'PS_DHE2_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',  # WHAT'S A DHE2?  NO SUCH ENGINE IN THE RSE BATCH
    },

    "(vehicle_data_df['drive_system'] == 1) & (vehicle_data_df['application_id'] == 'HLA')": {
        'GDI_TRX10_SS0': 'ICE_HLA_FWD_GDI_TRX10F_SS0',
        'TDS_TRX10_SS0': 'ICE_HLA_FWD_TDS_TRX10F_SS0',

        'TDS_TRX12_SS0': 'ICE_HLA_FWD_TDS_TRX12F_SS0',
        'TDS_TRX12_SS1': 'ICE_HLA_FWD_TDS_TRX12F_SS1',
        'GDI_TRX12_SS0': 'ICE_HLA_FWD_GDI_TRX12F_SS0',
        'GDI_TRX12_SS1': 'ICE_HLA_FWD_GDI_TRX12F_SS1',
        'GDI_DEAC_D_TRX12_SS0': 'ICE_HLA_FWD_GDI_DEAC_D_TRX12F_SS0',
        'GDI_DEAC_D_TRX12_SS1': 'ICE_HLA_FWD_GDI_DEAC_D_TRX12F_SS1',
        'MIL_TRX12_SS0': 'ICE_SLA_FWD_MILLER_TRX12F_SS0',  # no HLA MILLER at this time, possible misassignment or need new sims
        'MIL_TRX12_SS1': 'ICE_SLA_FWD_MILLER_TRX12F_SS1',  # no HLA MILLER at this time, possible misassignment or need new sims

        'TDS_TRX22_SS0': 'ICE_HLA_FWD_TDS_TRX22F_SS0',
        'TDS_TRX22_SS1': 'ICE_HLA_FWD_TDS_TRX22F_SS1',
        'GDI_TRX22_SS0': 'ICE_HLA_FWD_GDI_TRX22F_SS0',
        'GDI_TRX22_SS1': 'ICE_HLA_FWD_GDI_TRX22F_SS1',
        'GDI_DEAC_D_TRX22_SS0': 'ICE_HLA_FWD_GDI_DEAC_D_TRX22F_SS0',
        'GDI_DEAC_D_TRX22_SS1': 'ICE_HLA_FWD_GDI_DEAC_D_TRX22F_SS1',
        'MIL_TRX22_SS0': 'ICE_SLA_FWD_MILLER_TRX22F_SS0',  # no HLA MILLER at this time, possible misassignment or need new sims
        'MIL_TRX22_SS1': 'ICE_SLA_FWD_MILLER_TRX22F_SS1',  # no HLA MILLER at this time, possible misassignment or need new sims

        'FCV': 'FCV',

        'BEV': 'BEV_FWD',

        'PHEV': 'P2_PHEV_HLA_FWD_GDI_TRX12F_SS1_AER0',
        # for now... we might need to add one for something like BMW i3 REX

        'PS_MIL_TRXCV': 'PS_SLA_FWD_MILLER_TRXECVTF_SS1',  # no HLA PS at this time, possible misassignment or need new sims
        'PS_DHE_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',  # no HLA PS at this time, possible misassignment or need new sims
        'PS_DHE2_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',  # WHAT'S A DHE2?  NO SUCH ENGINE IN THE RSE BATCH  # no HLA PS at this time, possible misassignment or need new sims
    },

    "(vehicle_data_df['drive_system'] == 2) & (vehicle_data_df['application_id'] == 'HLA')": {
        'GDI_TRX10_SS0': 'ICE_HLA_RWD_GDI_TRX10R_SS0',
        'TDS_TRX10_SS0': 'ICE_HLA_RWD_TDS_TRX10R_SS0',

        'TDS_TRX12_SS0': 'ICE_HLA_RWD_TDS_TRX12R_SS0',
        'TDS_TRX12_SS1': 'ICE_HLA_RWD_TDS_TRX12R_SS1',
        'GDI_TRX12_SS0': 'ICE_HLA_RWD_GDI_TRX12R_SS0',
        'GDI_TRX12_SS1': 'ICE_HLA_RWD_GDI_TRX12R_SS1',
        'GDI_DEAC_D_TRX12_SS0': 'ICE_HLA_RWD_GDI_DEAC_D_TRX12R_SS0',
        'GDI_DEAC_D_TRX12_SS1': 'ICE_HLA_RWD_GDI_DEAC_D_TRX12R_SS1',
        'MIL_TRX12_SS0': 'ICE_SLA_RWD_MILLER_TRX12R_SS0',  # no HLA MILLER at this time
        'MIL_TRX12_SS1': 'ICE_SLA_RWD_MILLER_TRX12R_SS1',  # no HLA MILLER at this time

        'TDS_TRX22_SS0': 'ICE_HLA_RWD_TDS_TRX22R_SS0',
        'TDS_TRX22_SS1': 'ICE_HLA_RWD_TDS_TRX22R_SS1',
        'GDI_TRX22_SS0': 'ICE_HLA_RWD_GDI_TRX22R_SS0',
        'GDI_TRX22_SS1': 'ICE_HLA_RWD_GDI_TRX22R_SS1',
        'GDI_DEAC_D_TRX22_SS0': 'ICE_HLA_RWD_GDI_DEAC_D_TRX22R_SS0',
        'GDI_DEAC_D_TRX22_SS1': 'ICE_HLA_RWD_GDI_DEAC_D_TRX22R_SS1',
        'MIL_TRX22_SS0': 'ICE_SLA_RWD_MILLER_TRX22R_SS0',  # no HLA MILLER at this time, possible misassignment or need new sims
        'MIL_TRX22_SS1': 'ICE_SLA_RWD_MILLER_TRX22R_SS1',  # no HLA MILLER at this time, possible misassignment or need new sims

        'FCV': 'FCV',

        'BEV': 'BEV_RWD',

        'PHEV': 'P2_PHEV_HLA_RWD_GDI_TRX12R_SS1_AER0',
        # for now... we might need to add one for something like BMW i3 REX

        # ONLY FWD PS SO FAR...
        'PS_MIL_TRXCV': 'PS_SLA_FWD_MILLER_TRXECVTF_SS1',  # no HLA PS at this time, possible misassignment or need new sims
        'PS_DHE_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',  # no HLA PS at this time, possible misassignment or need new sims
        'PS_DHE2_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',  # WHAT'S A DHE2?  NO SUCH ENGINE IN THE RSE BATCH  # no HLA PS at this time, possible misassignment or need new sims
    },

    "(vehicle_data_df['drive_system'] == 4) & (vehicle_data_df['application_id'] == 'HLA')": {
        'GDI_TRX10_SS0': 'ICE_HLA_AWD_GDI_TRX10R_SS0',
        'TDS_TRX10_SS0': 'ICE_HLA_AWD_TDS_TRX10R_SS0',

        'TDS_TRX12_SS0': 'ICE_HLA_AWD_TDS_TRX12R_SS0',
        'TDS_TRX12_SS1': 'ICE_HLA_AWD_TDS_TRX12R_SS1',
        'GDI_TRX12_SS0': 'ICE_HLA_AWD_GDI_TRX12R_SS0',
        'GDI_TRX12_SS1': 'ICE_HLA_AWD_GDI_TRX12R_SS1',
        'GDI_DEAC_D_TRX12_SS0': 'ICE_HLA_AWD_GDI_DEAC_D_TRX12R_SS0',
        'GDI_DEAC_D_TRX12_SS1': 'ICE_HLA_AWD_GDI_DEAC_D_TRX12R_SS1',
        'MIL_TRX12_SS0': 'ICE_SLA_AWD_MILLER_TRX12R_SS0',  # no HLA MILLER at this time, possible misassignment or need new sims
        'MIL_TRX12_SS1': 'ICE_SLA_AWD_MILLER_TRX12R_SS1',  # no HLA MILLER at this time, possible misassignment or need new sims

        'TDS_TRX22_SS0': 'ICE_HLA_AWD_TDS_TRX22R_SS0',
        'TDS_TRX22_SS1': 'ICE_HLA_AWD_TDS_TRX22R_SS1',
        'GDI_TRX22_SS0': 'ICE_HLA_AWD_GDI_TRX22R_SS0',
        'GDI_TRX22_SS1': 'ICE_HLA_AWD_GDI_TRX22R_SS1',
        'GDI_DEAC_D_TRX22_SS0': 'ICE_HLA_AWD_GDI_DEAC_D_TRX22R_SS0',
        'GDI_DEAC_D_TRX22_SS1': 'ICE_HLA_AWD_GDI_DEAC_D_TRX22R_SS1',
        'MIL_TRX22_SS0': 'ICE_SLA_AWD_MILLER_TRX22R_SS0',  # no HLA MILLER at this time, possible misassignment or need new sims
        'MIL_TRX22_SS1': 'ICE_SLA_AWD_MILLER_TRX22R_SS1',  # no HLA MILLER at this time, possible misassignment or need new sims

        'FCV': 'FCV',

        'BEV': 'BEV_AWD',

        'PHEV': 'P2_PHEV_HLA_AWD_GDI_TRX12R_SS1_AER0',
        # for now... we might need to add one for something like BMW i3 REX

        # ONLY FWD PS SO FAR...
        'PS_MIL_TRXCV': 'PS_SLA_FWD_MILLER_TRXECVTF_SS1',  # no HLA PS at this time, possible misassignment or need new sims
        'PS_DHE_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',  # no HLA PS at this time, possible misassignment or need new sims
        'PS_DHE2_TRXCV': 'PS_SLA_FWD_DHE_TRXECVTF_SS1',  # WHAT'S A DHE2?  NO SUCH ENGINE IN THE RSE BATCH  # no HLA PS at this time, possible misassignment or need new sims
    },

}

ldv_map['drive_system'] = {1: 'FWD', 2: 'RWD', 4: 'AWD'}

ldv_map['cert_fuel_id'] = {"{'gasoline':1.0}": 'gasoline', "{'diesel':1.0}": 'diesel',
                           "{'hydrogen':1.0}": 'hydrogen', "{'electricity':1.0}": 'electricity'}

mdv_map['cost_curve_class'] = {
    'MIL_TRX12_SS0': 'MDV_ICE_HLA_RWD_DIESEL_TRX10R_SS0',
    'GDI_TRX12_SS0': 'MDV_ICE_HLA_RWD_PFI_TRX10R_SS0',  # NO GDI OPTION IN MDV RSE BATCH ...
}

mdv_map['drive_system'] = {1: 'FWD', 2: 'RWD', 4: 'AWD'}

mdv_map['cert_fuel_id'] = {"{'gasoline':1.0}": 'gasoline', "{'diesel':1.0}": 'diesel',
                           "{'hydrogen':1.0}": 'hydrogen', "{'electricity':1.0}": 'electricity'}

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
            xdv_map = mdv_map
        else:
            xdv_map = ldv_map

        try:
            for col in xdv_map:
                for condition_key in xdv_map[col]:
                    if 'vehicle_data_df' in str(condition_key):
                        condition = eval(condition_key)

                        if any(condition):
                            vehicle_data_df.loc[condition, [col]] = vehicle_data_df.loc[condition, [col]].replace(xdv_map[col][condition_key])
                    else:
                        vehicle_data_df.loc[:, [col]] = vehicle_data_df.loc[:, [col]].replace(xdv_map[col])
        except:
            print('wtf?')

        output_filename = 'remapped_%s.csv' % input_filename

        print('saving %s ...' % output_filename)

        # write template header
        template_header.to_csv(output_filename, header=False, index=False)

        # write data
        vehicle_data_df.to_csv(output_filename, mode='a', header=True, index=False)

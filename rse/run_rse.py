import os
import shutil
import sys
from datetime import datetime
# import time

from matplotlib import pyplot as plt, image as mpimg
from rse_functions import *
from tech_flags import *
import pandas as pd
from pathlib import Path
from tkinter import filedialog as fd

loop = True
# User setting to pause and view RSE check plots after each file is processed.
plot_view = False
# User setting to output RSE check plots as a single file for each input file processed.
plot_output = True


def generate_check_plot(validation_df, y_values, plot_num):
    """
        Generate check plot

    Parameters
    ----------
    validation_df (dataframe): RSE input and output validation data
    plot_num (int): plot number

    """

    # Generate check plot
    if plt.fignum_exists(plot_num):
        fig = plt.figure(plot_num)
        ax1 = fig.axes[0]
        ax1.lines[0].set_xdata(validation_df[y_values[plot_num] + "-ALPHA"])
        ax1.lines[0].set_ydata(validation_df[y_values[plot_num] + "-RSE"])

        if not all(validation_df[y_values[plot_num] + "-ALPHA"] == validation_df[y_values[plot_num] + "-RSE"]):
            z = np.polyfit(validation_df[y_values[plot_num] + "-ALPHA"], validation_df[y_values[plot_num] + "-RSE"], 1)
            p = np.poly1d(z)

            if len(ax1.lines) == 1:
                ax1.plot(validation_df[y_values[plot_num] + "-ALPHA"], p(validation_df[y_values[plot_num] + "-ALPHA"]),
                         color="black")
            else:
                ax1.lines[1].set_xdata(validation_df[y_values[plot_num] + "-ALPHA"])
                ax1.lines[1].set_ydata(p(validation_df[y_values[plot_num] + "-ALPHA"]))
        else:
            if len(ax1.lines) > 1:
                ax1.lines[1].remove()

        ax1.relim()
        ax1.autoscale_view()
    else:
        fig = plt.figure(plot_num)
        ax1 = fig.add_subplot()
        font1 = {'family': 'arial', 'color': 'black', 'size': 20}
        font2 = {'family': 'arial', 'color': 'black', 'size': 15}
        # Add titles to plot
        ax1.set_title(y_values[plot_num], fontdict=font1)
        ax1.set_xlabel(y_values[plot_num] + "-ALPHA", fontdict=font2)
        ax1.set_ylabel(y_values[plot_num] + "-RSE", fontdict=font2)
        ax1.grid()
        # validation_df.plot(y_values[plot_num] + "-ALPHA", y_values[plot_num] + "-RSE", style='o', legend=None, color="black")
        ax1.plot(validation_df[y_values[plot_num] + "-ALPHA"], validation_df[y_values[plot_num] + "-RSE"], 'ko')
        # Calculate equation for trend line

        if not all(validation_df[y_values[plot_num] + "-ALPHA"] == validation_df[y_values[plot_num] + "-RSE"]):
            z = np.polyfit(validation_df[y_values[plot_num] + "-ALPHA"], validation_df[y_values[plot_num] + "-RSE"], 1)
            p = np.poly1d(z)
            # Add trend line to plot
            ax1.plot(validation_df[y_values[plot_num] + "-ALPHA"], p(validation_df[y_values[plot_num] + "-ALPHA"]),
                     color="black")

    fig.savefig('plot' + str(plot_num) + '.png')


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


def create_output_files(input_filepathname, equation_df, validation_df, alpha_df):
    """
        Create output Excel workbook

    Parameters
    ----------
    input_filepathname (str): input file pathname
    equation_df (dataframe): equation data
    validation_df (dataframe): RSE input and output validation data
    alpha_df (dataframe): raw ALPHA input data

    Returns
    -------
        List of output file pathnames

    """
    # Strip off .csv and add .xlsx to ALPHA filename
    output_filepathname = Path(input_filepathname)
    output_filepathname = output_filepathname.with_suffix('')
    output_filepathname = output_filepathname.with_suffix('.xlsx')

    # Write out Excel workbook file with multiple worksheets
    writer = pd.ExcelWriter(output_filepathname, engine='xlsxwriter')

    # Write Equation worksheet
    equation_df.to_excel(writer, sheet_name='Equation')
    worksheet = writer.sheets['Equation']
    worksheet.autofit()

    # Write out Data worksheet
    validation_df.to_excel(writer, sheet_name='Data')
    worksheet = writer.sheets['Data']
    worksheet.autofit()

    # Write original ALPHA data
    alpha_df.to_excel(writer, sheet_name='ALPHA_Input', index=False)
    worksheet = writer.sheets['ALPHA_Input']
    worksheet.autofit()

    # Write out check plots
    workbook = writer.book
    for i, _ in enumerate(y_values):
        workbook.add_worksheet('Plot ' + str(i))
        worksheet = writer.sheets['Plot ' + str(i)]
        plot_name = 'plot' + str(i) + '.png'
        worksheet.insert_image('A1', plot_name)

    writer.close()

    return [output_filepathname]  # , rse_filepathname]


def file_cleanup(file_path, image_files, output_filepathnames):
    """
        Delete image files and relocate output file to "Completed" folder

    Parameters
    ----------
    file_path (str): file path of input directory
    image_files (list): list of image file names
    output_filepathnames (list): output file pathnames

    """
    # Delete check plot files
    for image_file in image_files:
        if os.path.exists(image_file):
            os.remove(image_file)

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

    # Move completed output file to 'Completed' subdirectory
    for ofn in output_filepathnames:
        shutil.move(ofn, new_directory_path + os.sep + ofn.name)

    return new_directory_path


def get_image_file_names(y_values):
    """
        Create list of image file names

    Parameters
    ----------
        y_values (list): names of y values

    Returns
    -------
        list of image files

    """

    image_files = []

    # Load check plot files
    for i, _ in enumerate(y_values):
        plot_name = 'plot' + str(i) + '.png'
        image_files.append(plot_name)

    return image_files


def generate_rses_and_plots(input_df, plot_output):
    """
        Generate response surface equations and validation plots.

    Parameters
    ----------
        input_df (dataframe): input data

    Returns
    -------
        tuple: dataframe of equations, dataframe of validation data

    """
    # Get input data columns from input file (x)
    x_data = []
    for i, _ in enumerate(x_values):
        x_data.append(input_df[x_values[i]])

    # Generate RSE equations iterating through all output values (y)
    validation_df = pd.DataFrame()
    equation_list = []
    count = 0
    for y_value in y_values:
        y = input_df[y_value]

        try:
            equ, rse = iterate1(x_data, y, x_values)
        except:
            print('*** could not process %s signal "%s"' % (input_filepathname, y_value))
            y.update(np.zeros_like(y))
            equ, rse = iterate1(x_data, y, x_values)

        if count == 0:
            for i, _ in enumerate(x_values):
                validation_df.insert(i, x_values[i], x_data[i], True)

        # Add original and RSE output data to dataframe
        validation_df[y_values[count] + "-ALPHA"] = y
        validation_df[y_values[count] + "-RSE"] = rse

        generate_check_plot(validation_df, y_values, count)

        if rse.min() == rse.max():
            equ = '(%f)' % rse.min()  # parens so column gets treated as string and not numeric

        # Add equation to array
        equation_list.append(equ)
        count += 1

    # Create dataframe of equations
    equation_df = pd.DataFrame({"Value": y_values, "Equation": equation_list})

    return equation_df, validation_df


while loop:
    # Open file dialog for ALPHA input file
    input_files = fd.askopenfilenames(title="Open ALPHA Results File",
                                    filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*")))

    input_files = [i for i in input_files if 'configuration' not in i]

    if input_files:
        for input_filepathname in input_files:
            input_filename = get_filename(input_filepathname)

            print('processing %s ...' % input_filename)

            # Save the path of the selected input file
            file_path = os.path.dirname(input_filepathname)

            os.chdir(file_path)
            config_file = [cf for cf in os.listdir() if 'configuration' in cf if cf.endswith('.csv')][0]

            # Create path to configuration file in the same directory as the input file
            config_path = os.path.join(file_path, config_file)

            # Exit if file error or user cancels dialog
            if not os.path.exists(input_filepathname):
                sys.exit()

            # Read RSE input and output values from configuration file
            config_df = pd.read_csv(config_path)
            x_values = config_df['rse_terms'].dropna()
            candidate_y_values = config_df['alpha_outputs'].dropna()

            y_values = []
            y_names = []
            for i, cyv in enumerate(candidate_y_values):
                if 'condition' in config_df and pd.notna(config_df['condition'][i]) and eval(config_df['condition'][i]):
                    y_values.append(cyv)
                    y_names.append(config_df['omega_inputs'][i])
                elif 'condition' not in config_df and pd.notna(config_df['omega_inputs'][i]):
                    y_values.append(cyv)
                    y_names.append(config_df['omega_inputs'][i])

            rename_dict = dict(zip(y_values, y_names))

            # Read ALPHA data, skipping second row of units
            input_df = pd.read_csv(input_filepathname, skiprows=[1])

            # rename columns
            for k, v in rename_dict.items():
                if not pd.isna(v):
                    if '=' in v:
                        rename, value = v.replace(' ', '').split('=')
                        input_df[k] = eval(value)
                        rename_dict[k] = rename

            equation_df, validation_df = generate_rses_and_plots(input_df, plot_output)

            equation_df.replace(rename_dict, inplace=True)  # rename values

            # Read the ALPHA file into dataframe
            alpha_df = pd.read_csv(input_filepathname)

            output_filepathnames = create_output_files(input_filepathname, equation_df, validation_df, alpha_df)

            image_files = get_image_file_names(y_values)

            if plot_output:  # Combine RSE check plots into a single file if desired.
                # Specify the output file path
                output_file = input_filename + '.png'
                # Specify the grid size
                grid_size = (4, 4)
                # Combine the images into a single file
                combine_images(image_files, output_file, grid_size)
                # Get the absolute path of the current input file and add suffix of image file
                file_path_1 = Path(input_filepathname)
                file_path_1 = file_path_1.with_suffix('')
                file_path_1 = file_path_1.with_suffix('.png')
                # Append image file to list of files to be processed
                output_filepathnames.append(file_path_1)

                if plot_view:
                    # Load the image file
                    image_path = input_filename + ".png"
                    image = mpimg.imread(image_path)

                    # Create a figure with the desired size
                    fig = plt.figure(figsize=(10, 8))

                    # Display the image
                    plt.imshow(image)

                    # Hide the axis
                    plt.axis('off')
                    plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
                    plt.title('ALPHA vs RSE for: ' + input_filename)

                    # Show the plot
                    # plt.tight_layout
                    plt.show()

            output_folderpath = file_cleanup(file_path, image_files, output_filepathnames)

        os.chdir(output_folderpath)
        rse_files = [f for f in os.listdir() if '.xlsx' in f]

        print('')

        collated_rse_df = pd.DataFrame()
        processed = []
        for rse_file in rse_files:
            rse_filename = rse_file[20:]  # drop timestamp
            concat_file = False

            if '_PHEV_' in input_filename:
                for other_file in [f for f in rse_files if f != rse_file and f not in processed]:
                    other_filename = other_file[20:]  # drop timestamp
                    if rse_filename.replace('_CD_', '_CS_') == other_filename:
                        cd_df = pd.read_excel(rse_file, 'Equation', index_col=1).transpose().drop('Unnamed: 0').reset_index()
                        cd_df.rename({'index': 'cost_curve_class'}, axis=1, inplace=True)

                        cs_df = pd.read_excel(other_file, 'Equation', index_col=1).transpose().drop('Unnamed: 0').reset_index()

                        rse_name = rse_filename.replace('_CD_', '_').\
                            replace(config_df['alpha_prefix'][0], '').\
                            replace('_results', '').\
                            replace('.xlsx', '')

                        print('collating PHEV %s...' % rse_name)

                        rse_df = pd.concat([cd_df, cs_df.drop(columns='index')], axis=1).drop_duplicates()

                        processed.extend([rse_file, other_file])

                        concat_file = True
            else:
                concat_file = True

                rse_df = pd.read_excel(rse_file, 'Equation', index_col=1).transpose().drop('Unnamed: 0').reset_index()
                rse_df.rename({'index': 'cost_curve_class'}, axis=1, inplace=True)

                rse_name = rse_filename.\
                    replace(config_df['alpha_prefix'][0], ''). \
                    replace('_results', ''). \
                    replace('.xlsx', '')
                print('collating %s...' % rse_name)

            if concat_file:
                rse_df['cost_curve_class'] = rse_name
                rse_df = apply_tech_flags(rse_df, rse_name)

                collated_rse_df = pd.concat([collated_rse_df, rse_df])

        collated_filename = '%s_%s_%s.csv' % (get_filename(file_path),
                                              config_df['batch_prefix'][0],
                                              datetime.now().strftime('%Y_%m_%d'))

        print('\nwriting %s ...\n' % collated_filename)

        collated_rse_df.sort_values('cost_curve_class').to_csv(collated_filename, index=False)

    else:
        loop = False

    plt.close('all')
    # The main while loop continues

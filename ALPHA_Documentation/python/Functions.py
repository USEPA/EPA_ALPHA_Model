# The following section demonstrates how to insert a header into the code file
# that will be recorded when the auto-documentation is built.
# "Functions" will be the name of the sub-heading in the documentation using the
# formatting shown.

"""Functions
   ---------

   The ``functions.py`` file demonstrates how to auto-document functions

   """

import os
import shutil
import sys

# The following section demonstrates how to comment functions
# that will be recorded when the auto-documentation is built.


def validate_folder(dstfolder):
    """
    Verify the existence of dstfolder and try to create it if doesn't exist

    .. code-block:: python

        validate_folder('C:\\Users\\Temp')

    :param dstfolder: Path the folder to validate/create

    .. attention:: Exits app on failure
    """
    if not os.access(dstfolder, os.F_OK):
        try:
            os.makedirs(dstfolder, exist_ok=True)  # try create folder if necessary
        except:
            print("Couldn't access or create {}".format(dstfolder), file=sys.stderr)
            exit(-1)


def validate_file(filename):
    """
    Verify the existence of filename and try to create it if doesn't exist

    :param filename: File pathname of the file to validate

    .. attention:: Exits app on failure
    """
    if not os.access(filename, os.F_OK):
        print("\n*** Couldn't access {}, check path and filename ***".format(filename), file=sys.stderr)
        exit(-1)


def get_filepath(filename):
    """
    Returns path to file, e.g. /somepath/somefile.txt -> /somepath

    :param filename: file name, including path to file as required
    :return: file path, not including the file name
    """
    return os.path.split(filename)[0]


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


def get_filenameext(filename):
    """
    Returns file name including extension, e.g. /somepath/somefile.txt -> somefile.txt

    :param filename: file name, including extension, including path to file as required
    :return: file name including extension
    """
    return os.path.split(filename)[1]




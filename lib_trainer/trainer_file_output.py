#!/usr/bin/env python3


"""

Contains all the file output logic for the trainer

"""


import os
import errno


def make_sure_path_exists(path):
    """
    Create a directory if one does not already exist

    Will re-raise any exceptions and send them back to the calling program
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        # It's totally ok if we can't create the directory because it already
        # exists
        if exception.errno != errno.EEXIST:
            raise OSError from exception


def make_directories_from_list(directory_listing):
    """
    Creates all the directories from a list of files

    Returns:
        True: If Sucessful
        False: If an error occured

    """
    try:
        for path in directory_listing:
            make_sure_path_exists(path)
    except OSError as exception:
        print("Error creating the directories to save the results")
        print(str(exception))
        return False
    return True


def create_rule_folders(base_directory):
    """
    Creates all the folders for saving a pcfg rule to disk

    Will create all files in the folder specified by base directory

    Returns:
        True: If Sucessful
        False: If an error occured

    """

    # Set up the list of all the directories to create
    directory_listing = [base_directory]

    return make_directories_from_list(directory_listing)

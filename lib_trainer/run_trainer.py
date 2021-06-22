#!/usr/bin/env python3


"""

Responsible for running the top level training session

Moving this here to get it out of the main() function

"""

import sys
import traceback
from collections import Counter

# Local imports
from lib_trainer.trainer_file_input import TrainerFileInput
from lib_trainer.trainer_file_input import get_confirmation


def run_trainer(program_info, base_directory):
    """
    Runs through the input and generates the Markov Grammar

    This function is also responsible for saving the grammar to disk

    Variables:
        program_info: A dictionary containing all of the command line
        option results

        base_directory: The base directory to save the resulting grammar to

    Return:
        True: If the operations completed sucessfully
        False: If any errors occured
    """

    print("-------------------------------------------------")
    print("Training the Markov Grammae")
    print("-------------------------------------------------")
    print("")

    # Initialize the file input to read passwords from
    file_input = TrainerFileInput(
                    program_info['training_file'],
                    program_info['encoding'])

    # Used for progress_bar
    num_parsed_so_far = 0
    print("Printing out status after every million passwords parsed")
    print("------------")

    ## Loop until we hit the end of the file
    try:
        password = file_input.read_password()
        while password:

            # Print status indicator if needed
            num_parsed_so_far += 1
            if num_parsed_so_far % 1000000 == 0:
                print(str(num_parsed_so_far//1000000) +' Million')

            # Get the next password
            password = file_input.read_password()

    except Exception as msg:
        print("Exception: " + str(msg))
        return False

    # Record how many valid passwords there were
    num_valid_passwords = file_input.num_passwords

    if num_valid_passwords == 0:
        print()
        print("Error, no valid passwords were found when attempting to train ruleset.")
        return False

    # Print some basic statistics after first loop
    print()
    print("Number of Valid Passwords: " + str(num_valid_passwords))
    print("Number of Encoding Errors Found in Training Set:" + str(file_input.num_encoding_errors))
    print()

    # Perform duplicate detection and warn user if no duplicates were found
    if not file_input.duplicates_found:
        print()
        print("WARNING:")
        print("    No duplicate passwords were detected in the first " +
            str(file_input.num_to_look_for_duplicates) + " parsed passwords")
        print()
        print("    This may be a problem since the training program needs to know frequency")
        print("    info such as '123456' being more common than '629811'")
        if get_confirmation("Do you want to exit and try again with a different training set (RECOMENDED)"):
            return False
    # Everything appears to have completed successfully
    return True
'''
    print()
    print("-------------------------------------------------")
    print("Saving Data")
    print("-------------------------------------------------")
    print()

    # Save the configuration file
    if not save_config_file(base_directory,program_info, file_input, pcfg_parser):
        print("Error, something went wrong saving the configuration file to disk")
        return False

    # Save the OMEN data
    if not save_omen_rules_to_disk(
        omen_trainer,
        omen_keyspace,
        omen_levels_count,
        num_valid_passwords,
        base_directory,
        program_info
        ):
        print("Error, something went wrong saving the OMEN data to disk")
        return False

    # Save the pcfg data to disk
    if not save_pcfg_data(
                base_directory,
                pcfg_parser,
                program_info['encoding'],
                program_info['save_sensitive'],
            ):
        print("Error, something went wrong saving the pcfg data to disk")
        return False

    # Print statisticts to the screen
    print_statistics(pcfg_parser)
'''

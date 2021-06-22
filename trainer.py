#!/usr/bin/env python3


"""

Name: IMPROV Trainer
-- Training program that creates a Markov probability list for password cracking

Copyright 2021 Matt Weir

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Contact Info: cweir@vt.edu

"""


# Including this to print error message if python < 3.0 is used
from __future__ import print_function
import sys
# Check for python3 and error out if not
if sys.version_info[0] < 3:
    print("This program requires Python 3.x", file=sys.stderr)
    sys.exit(1)

import argparse
import os

# Local imports
from lib_trainer.banner_info import print_banner
from lib_trainer.trainer_file_input import detect_file_encoding

from lib_trainer.run_trainer import run_trainer

from lib_trainer.trainer_file_output import create_rule_folders


def parse_command_line(program_info):
    """
    Responsible for parsing the command line.

    Note: This is a fairly standardized format that I use in many of my programs

    Variables:

        program_info: A dictionary that contains the default values of
        command line options. Results overwrite the default values and the
        dictionary is returned after this function is done.

    If successful, returns True, returns False if value error, program exits if
    argparse catches a problem.
    """

    # Keeping the title text to be generic to make re-using code easier
    parser = argparse.ArgumentParser(
        description= program_info['name'] +
        ', version: ' +
        program_info['version']
    )

    ## Standard options for filename, encoding, etc
    #
    # The rule name to save the grammar as. This will create a directory of
    # this name.
    parser.add_argument(
        '--rule',
        '-r',
        help = 'Name of generated ruleset. Default is ' +
        program_info['rule_name'],
        metavar = 'RULESET_NAME',
        required = False,
        default = program_info['rule_name']
    )

    # The training file of passwords to train on
    parser.add_argument(
        '--training',
        '-t',
        help = 'The training set of passwords to train from',
        metavar = 'TRAINING_SET',
        required = True
    )

    # The file encoding of the training file
    parser.add_argument(
        '--encoding',
        '-e',
        help = 'File encoding to read the input training set. If not ' +
        'specified autodetect is used',
        metavar = 'ENCODING',
        required = False
    )

    # Any comments someone may want to add to the training file
    parser.add_argument(
        '--comments',
        help = 'Comments to save in the rule configuration file, encapsulated in quotes ""',
        metavar = '"COMMENTS"',
        required = False,
        default = program_info['comments']
    )

    # Parse all the args and save them
    args=parser.parse_args()
    # Standard Options
    program_info['rule_name'] = args.rule
    program_info['training_file'] = args.training
    program_info['encoding']= args.encoding
    program_info['comments'] = args.comments

    return True


def main():
    """

    Main function, starts everything off

    Responsible for calling the command line parser, detecting the
    encoding of the training set, creating the initial folders
    and then kicking off the training via run_trainer()

    """

    # Information about this program
    program_info = {

        # Program and Contact Info
        'name':'IMPROV Trainer',
        'version': '1.0',
        'author':'Matt Weir',
        'contact':'cweir@vt.edu',

        # Standard Options
        'rule_name':'Default',
        'training_file':None,
        'encoding':None,
        'comments':'',

    }

    print_banner()
    print("Version: " + str(program_info['version']))

    # Parsing the command line
    if not parse_command_line(program_info):
        # There was a problem with the command line so exit
        print("Exiting...")
        return

    ## Set the file encoding for the training set
    #
    # If NOT specified on the command line by the user run an autodetect
    if program_info['encoding'] is None:
        print()
        print("-----------------------------------------------------------------")
        print("Attempting to autodetect file encoding of the training passwords")
        print("-----------------------------------------------------------------")

        possible_file_encodings = []
        if not detect_file_encoding(
            program_info['training_file'],
            possible_file_encodings
        ):
            print("Exiting...")
            return

        # Select the most likely file encoding
        program_info['encoding'] = possible_file_encodings[0]

    ## Create Rules folder for the saved grammar
    #
    # Doing this before parsing the input file further since if a permission
    # error occurs here want to fail fast vs. waiting 10 minutes to finialize
    # parsing the data

    # Get the base directory to save all the data
    #
    # Don't want to use the relative path since who knows where someone is
    # invoking this script from
    #
    # Also aiming to make this OS independent
    #
    base_directory = os.path.join(
                        os.path.dirname(os.path.realpath(__file__)),
                        'Rules',
                        program_info['rule_name'])

    if not create_rule_folders(base_directory):
        print("Exiting...")
        return

    # Start training the ruleset
    if not run_trainer(program_info, base_directory):
        print("The training did not complete successfully. Exiting")


if __name__ == "__main__":
    main()

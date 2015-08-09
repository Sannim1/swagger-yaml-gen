#! /usr/bin/python
import os

def get_spec_file():
    """
        Returns a file object pointing to the original spec.yaml file
    """
    spec_file_path = os.getcwd() + '/spec.yaml'
    file_handle = open(spec_file_path)

    return file_handle

def get_spec_paths():
    """
        Gets all path specifications in the respective ".yaml" files
        residing in the paths/ directory

        Returns these path specifications as a string
    """
    path_directory = os.getcwd() + '/paths'
    return read_yaml_files(path_directory)

def get_spec_definitions():
    """
        Gets all definition specifications in the respective ".yaml" files
        residing in the definitions/ directory

        Returns these path specifications as a string
    """
    definitions_directory = os.getcwd() + '/definitions'
    return read_yaml_files(definitions_directory)

def read_yaml_files(directory):
    """
        Reads all the ".yaml" files residing in a particular directory
        and concatenates them into a single string.

        Returns the contents of the ".yaml" files as a string
    """

    # checks if the supplied directory exists and is a valid directory path
    # returns an empty string otherwise
    if not os.path.isdir(directory):
        return ""

    # variable to hold output ".yaml" string
    out_yaml = ''

    # loop through all ".yaml" files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith(".yaml"):
            # append the contents of current ".yaml" file to output
            out_yaml += read_file(directory + '/' +file_name)

    # return output ".yaml" string
    return out_yaml

def read_file(file_path):
    """
        Reads all lines in a file

        Returns the contents of a file as a string
    """
    # verifies that file_path specified exists and is valid
    # returns an empty string otherwise
    if not os.path.isfile(file_path):
        return ""

    # variable to hold file contents
    file_contents = ''

    # open file for reading
    file_handle = open(file_path,'r')

    # loop through all lines in the file and append them to output string
    for line in file_handle:
        file_contents += line

    # append new line to end of string and return
    return file_contents + '\n'

def glue():
    """
        Main function that glues path and definition specifications into
        single file.

        Creates an output file "final_spec.yaml" containing
        path and definition specifications
    """

    # get file object referencing original spec file
    spec_file = get_spec_file()

    # delete any existing "final_spec.yaml" file(s) in current directory
    out_file_path = os.getcwd() + '/final_spec.yaml'
    if os.path.exists(out_file_path):
        os.remove(out_file_path)

    # create "final_spec.yaml" file
    out_file_flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    out_file = os.open(out_file_path, out_file_flags)

    # open "final_spec.yaml" for writing
    with os.fdopen(out_file, 'w') as out_file_object:
        # loop through original spec file
        for index, line in enumerate(spec_file):
            # check for path specification placeholder
            if '#$:PATHS' in line:
                # replace placeholder with actual path specifications
                out_file_object.write(get_spec_paths() + '\n')
                continue

            # check for definition specification placeholder
            if '#$:DEFINITIONS' in line:
                # replace placeholder with actual definition specifications
                out_file_object.write(get_spec_definitions() + '\n')
                continue

            # No placeholders on this line, copy original specifications
            # into new file
            out_file_object.write(line)

# Call glue method, when this file is executed
glue()
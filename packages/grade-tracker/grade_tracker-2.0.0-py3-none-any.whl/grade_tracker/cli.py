#!/usr/bin/env python3
"A Small Python CLI to track grades"

import sys
import argparse
from os.path import exists as file_exists
import yaml
from xdg import xdg_config_home, xdg_data_home

__version__ = "2.0.0"


def trunc(num: float, precision: int) -> str:
    """Truncates num so it has precision decimal places. Returns a string"""
    temp = str(num)
    for x in range(len(temp)):
        if temp[x] == '.':
            # x is the index of the decimal point
            try:
                # x+precision+1 is the index of the last number we
                # want to include. Therefore we return from the start
                # of the string to the end of the string
                return temp[:x+precision+1]
            except IndexError:
                # This error will occur if x+precision+1 is outside
                # the length of the string. In this case, we just
                # don't truncate the string at all.
                return temp
    # If we get here, there is no decimal place in the
    # number. Therefore we can just return it, assuming that it is an
    # integer.
    return temp


def get_config_file() -> str:
    """Get the path for the config file as a string.

    Looks for file in the following order:

    * xdg_config_home/gradeTracker/config.yml
    * ./config.yml

    If no config file is found, the user is shown an error message and
    the program exits.
    """

    xdg_config_file = str(xdg_config_home())+"/gradeTracker/config.yml"
    if file_exists(xdg_config_file):
        return xdg_config_file
    elif file_exists('config.yml'):
        return 'config.yml'
    else:
        print(('No config file found.'
               'Please place one at $XDG_CONFIG_HOME/gradeTracker/config.yml'),
              file=sys.stderr)
        sys.exit()


def get_data_file(config: dict) -> str:
    """Get the path for the data file as a string.

    Looks for file in the following order:

    * data_file variable set in config file (if it is set)
    * xdg_data_home/gradeTracker/data.yml
    * ./data.yml

    If the file set in the config file does not exist, the user is
    shown an error and the program exits

    If neither xdg_data_home/gradeTracker/data.yml or ./data.yml
    exist, the user is shown an error and the program exits
    """

    xdg_data_file = str(xdg_data_home())+"/gradeTracker/data.yml"
    if "data_file" in config:
        if file_exists(config["data_file"]):
            return config["data_file"]
        else:
            print((f'{config["data_file"]} is set as the data file but does not exist.\n'
                   'This must be an explicit path (i.e. does not contain ~ or environment variables)'),
                  file=sys.stderr)
            sys.exit()

    elif file_exists(xdg_data_file):
        return xdg_data_file
    elif file_exists('data.yml'):
        return 'data.yml'
    else:
        print('No data file found. Please place one at $XDG_DATA_HOME/gradeTracker/data.yml',
              file=sys.stderr)
        sys.exit()




def print_module_tree(module_dict: dict, prestring: str) -> None:
    """Prints a tree of modules from module_list to stdout.

    prestring will be put at the start of each message,
    and 2 spaces will be appended for each added layer"""
    for module in module_dict:
        fstring = (f'{prestring}{module["module"]} '
                   f'with weighting {module["weighting"]}{args.post_string}')
        # This string looks like '  moduleName with weighting xx%
        if 'percent' in module:
            fstring += f' and percentage {module["percent"]}{args.post_string}'
        print(fstring)
        if 'modules' in module:
            # This means there are submodules, so we should recurse into them
            print_module_tree(module["modules"], prestring+args.indent_string)


def check_module_tree(module_dict: dict) -> bool:
    """Checks the module tree inside module_dict is valid.

    If any subtree does not sum close to 100, the user will be shown
    an error and the program will exit. The sum has to be within
    args.total_weighting_tolerance of 100 to be valid.
    """

    # We want to sum all the weightings of the modules that are first
    # level elements of module_dict.
    total_weighting = 0
    for module in module_dict:
        total_weighting += module["weighting"]

        # We also want to check any submodules, so we recurse in
        if 'modules' in module:
            if check_module_tree(module["modules"]) is False:
                # We know that a module tree does not sum to 100, so
                # we tell the user there is an error and exit the
                # program.
                print(f"Config File Invalid \n{module['module']}'s submodules do not sum to 100%",
                      file=sys.stderr)
                sys.exit()

    # We have to allow some tolerance for the total weighting to be
    # away from 100%. This will give some small calculation errors,
    # but is needed in case a module has a weighting that is a
    # recurring decimal.
    if abs(total_weighting - 100) > args.total_weighting_tolerance:
        # Returning false here is equivalent to throwing an error.

        # TODO: It might be worth moving the error throwing to here
        # instead of at the next level
        return False


def calc_percentage(module_dict: dict, module_name: str, prestring: str) -> float:
    """Calculates the weighted average percentage inside module_dict.

    Additionally stores strings for printing in the global variable
    print_strings
    """

    # First we want to generate lists of all of the percentages and
    # weightings on this level
    percentages = []
    weightings = []

    # This an array of strings ready for later printing
    global print_strings

    # Check to see if print_strings has already been defined. If it
    # hasn't we need to define it to be an empty list
    if 'print_strings' not in globals():
        print_strings = []

    for module in module_dict:
        if 'modules' in module:
            # This module has submodules. Therefore the percent for
            # this module must be computed recursively.
            percent = calc_percentage(module['modules'], module['module'], prestring+args.indent_string)
        elif 'percent' in module:
            # This means there are no submodules, and we are therefore
            # at the bottom of the tree. Therefore we extrct the
            # percentage.
            percent = module["percent"]

            # We want the string to include 2 decimal places at
            # maximum, to make the output look nice.
            percent_string = trunc(percent, 2)
            print_strings.append(f"{prestring+args.indent_string}{module['module']}: "
                                 f"{percent_string}{args.post_string}")
        else:
            # This module currently has no percentage
            # applied. Therefore we just ignore the module.  This case
            # will occur if the module has not been marked yet.
            continue
        weighting = module["weighting"]
        percentages.append(percent)
        weightings.append(weighting)

    # If we want to ignore unmarked, we need to adjust the weightings
    # so that the total weighting is 100.
    if args.ignore_unmarked:
        # We need to find the scale factor to multiply each weighting
        # by so that the total is 100.
        total_weighting = sum(weightings)
        scale_factor = 100/total_weighting
        # Now we update weightings to be scaled by the scale factor
        for idx, weighting in enumerate(weightings):
            weightings[idx] = scale_factor*weighting

    # Now we have appropriate weightings, we can multiply the
    # weighting by the percentage to get the weighted percentages. We
    # also need to divide by 100 so that the weighted percentage stays
    # as a percentage.
    weightedPercentages = []
    for idx, percent in enumerate(percentages):
        weightedPercentages.append(percent*weightings[idx]/100)

    # The sum of the weighted percentages is the weighted average
    weighted_avg = sum(weightedPercentages)
    # We only want it to display at most 2 decimal places of the
    # weighted average. If we do not do this, it looks bad.
    weighted_avg_string = trunc(weighted_avg, 2)
    print_strings.append(f'{prestring}{module_name}: {weighted_avg_string}{args.post_string}')
    return weighted_avg


def check_data_dict(data: dict) -> None:
    """Checks whether the data is valid"""

    # This function wraps check_module_tree to check the overall data,
    # rather than just a specific tree.
    if check_module_tree(data["modules"]) is False:
        # If check_module_tree returns false, the tree does not sum to 100

        print("Data File Invalid \nRoot tree's percent does not sum to 100",
              file=sys.stderr)
        sys.exit()


def load_config() -> None:
    """Loads the config, combining CLI arguments and config file settings.

    Opens the config file, and checks it is valid YAML. If it is not,
    an error is shown.

    Merges config settings with the following priorities

    * Command Line Parameters
    * Config File Settings
    * Default Values

    Config settings are stored inside the global args.
    """

    # I want to parse the arguments here so I can set the default values from
    # the config file before running anything else
    global args
    args = parser.parse_args()

    # args.config_file has the default set in case the user does not
    # specify it on the command line
    with open(args.config_file, "r") as config_file:
        # Load the config file
        try:
            config = yaml.safe_load(config_file)
        except yaml.YAMLError as exc:
            # The yaml in the config is invalid. throw an error and
            # end the program.
            print("Config File Invalid, YAML processor returns:")
            print(exc, file=sys.stderr)
            sys.exit()

    # We couldn't set the default earlier because of run order, so
    # we now set it to it's default if it wasn't set as a CLI
    # argument.
    if args.data_file is None:
        args.data_file = get_data_file(config)

    # If the user has not set things on the command line, we want to
    # first check the config file, and if not use the default value

    if args.total_weighting_tolerance is None:
        if "total_weighting_tolerance" in config:
            args.total_weighting_tolerance = config["total_weighting_tolerance"]
        else:
            args.total_weighting_tolerance = 5

    if args.ignore_unmarked is None:
        if "ignore_unmarked" in config:
            args.ignore_unmarked = config["ignore_unmarked"]
        else:
            args.ignore_unmarked = True

    if args.indent_string is None:
        if "indent_string" in config:
            args.indent_string = config["indent_string"]
        else:
            args.indent_string = "  "

    if args.post_string is None:
        if "post_string" in config:
            args.post_string = config["post_string"]
        else:
            args.post_string = "%"


def open_data_file() -> dict:
    """Opens the data file and returns the data

    Open the data file in args.data_file, check that it is valid YAML,
    and check that the weightings sum as close to 100
    """
    with open(args.data_file, "r") as data_file:
        try:
            data = yaml.safe_load(data_file)
        except yaml.YAMLError as exc:
            # The yaml in the data is invalid, tell the user and end
            # the program
            print("Data File Invalid, YAML processor returns:")
            print(exc, file=sys.stderr)
            sys.exit()
        # Check the modules in the data file have total weighting near
        # to 100.
        check_data_dict(data)
    return data


def main():
    # Create a parser for arguments, and add the required possibilities.
    global parser
    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-c', '--config-file',
                        help='The file used for configuration',
                        default=get_config_file(),
                        dest='config_file')

    # The default for data file has to be none, as we want to check the
    # config file with high priority. However we have not loaded the
    # config file yet, so cannot do this.
    parser.add_argument('-d', '--data-file',
                        help='The file used for data',
                        default=None,
                        dest='data_file')

    parser.add_argument('--ignore-unmarked',
                        help='If enabled, gradeTracker will not assume that unmarked modules are 0.',
                        dest='ignore_unmarked',
                        default=None,
                        action='store_true')

    parser.add_argument('--use-unmarked',
                        help='If enabled, gradeTracker will assume that unmarked modules are 0.',
                        dest='ignore_unmarked',
                        default=None,
                        action='store_false')

    parser.add_argument('--indent-string',
                        help='String that should be used to indent each option. \"  \" by default',
                        dest='indent_string',
                        default=None)

    parser.add_argument('--post-string',
                        help='String that should be displayed after a grade is shown. \"%%\" by default',
                        dest='post_string',
                        default=None)

    parser.add_argument('--total-weighting-tolerance',
                        help='How close do we require the total weight to be to 100',
                        dest='total_weighting_tolerance',
                        default=None)

    parser.add_argument('-v', '--version',
                        action='version',
                        version="%(prog)s ("+__version__+")")

    parser.add_argument('command',
                        help='Command to run',
                        choices=['print-marks', 'print-modules', 'check-config'])

    # When the program first starts, we need to load the config and data
    # files.
    load_config()
    data = open_data_file()

    # Process the command the user gives.
    if args.command == 'print-marks':
        calc_percentage(data["modules"], 'Overall', '')
        # print_strings give us the right strings but upside down, so we reverse
        # them and then print them
        print_strings.reverse()
        for string in print_strings:
            print(string)

    elif args.command == 'print-modules':
        print_module_tree(data["modules"], "")

    elif args.command == 'check-config':
        # We've already checked the config is valid so we can just tell the user
        print("Config is valid")


if __name__ == "__main__":
    main()

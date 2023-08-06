This is a CLI written in python for tracking grades. It reads data from a yaml file

# Installation

Install this with
```
$ pip install grade-tracker
```

# The Data File

The data file, by default read from `$XDG_DATA_HOME/gradeTracker/data.yml` is a yaml file containing the data to calculate with. An example of this file can be found [in the github repository](https://www.github.com/dwdwdan/gradeTracker/blob/master/data.yml)

The file should always contain a `modules` key with a list of submodules. These submodules should have a `weighting` set which sums to 100 (this is checked when gradeTracker is run). This represents how much this module is worth.

The key `percent` represents the mark given out of 100 for that assignment. If not set, gradeTracker will ignore the module or assume it's 0 depending on `ignore_unmarked`

A module can also have submodules by including the `modules` tag, and following the same pattern. gradeTracker should deal with any depths, though it is not thoroughly tested will many layers.

# Configuration

Configuration is done in the yaml file `$XDG_CONFIG_HOME/gradeTracker/config.yml`. By default this is ​`~/.config/gradeTracker/config.yml`. An example of this file can be found [in the github repository](https://www.github.com/dwdwdan/gradeTracker/blob/master/config.yml). There are 5 possible options:

## ignore-unmarked

If set to true, gradeTracker will ignore variables without a mark attatched. If set to false, gradeTracker will assume they are 0. Defaults to true if unset.

## data-file

This is the file that gradeTracker will read to calculate percentages. If not set, it will default to `$XDG_DATA_HOME/gradeTracker/data.yml`

## indent-string

This is used each time gradeTracker indents. Default is `"  "`, but `"| "` also looks nice

## post-string

This is used after each mark is given. Defaults to `"%"`

## total-weightingtolerance

How close we require the total weighting to be to 100. This is so that fractional percentages can be properly used.

# Usage

The `gradeTracker` command has one required parameter, which is the command you would like to run. It has 3 options:

- `print-marks` will calculate and output a breakdown of marks, calculating the percentages at each module
- `print-modules` will output the module tree, showing the name,
    weighting and percent. This is essentially just reformatting the `data.yml` file.
- `check-config` will check the data file and config file for validity.

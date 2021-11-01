# --- Day 6: Probably a Fire Hazard ---
#
# Because your neighbors keep defeating you in the holiday house decorating contest
# year after year, you've decided to deploy one million lights in a 1000x1000 grid.
#
# Furthermore, because you've been especially nice this year, Santa has mailed
# you instructions on how to display the ideal lighting configuration.
#
# Lights in your grid are numbered from 0 to 999 in each direction; the lights at
# each corner are at 0,0, 0,999, 999,999, and 999,0. The instructions include
# whether to turn on, turn off, or toggle various inclusive ranges given as coordinate pairs.
# Each coordinate pair represents opposite corners of a rectangle, inclusive; a coordinate
# pair like 0,0 through 2,2 therefore refers to 9 lights in a 3x3 square. The lights
# all start turned off.
#
# To defeat your neighbors this year, all you have to do is set up your lights
# by doing the instructions Santa sent you in order.
#
# For example:
#
# turn on 0,0 through 999,999 would turn on (or leave on) every light.
# toggle 0,0 through 999,0 would toggle the first line of 1000 lights, turning
# off the ones that were on, and turning on the ones that were off.
# turn off 499,499 through 500,500 would turn off (or leave off) the middle four lights.
# After following the instructions, how many lights are lit?

# NOTES:
# This is reminiscent of "On Off" coding used on old TV broadcasts.
# Rather than code every pixel, write "start/stop" instructions.
#
# THIS is very slow and could be improved dramatically.

# IMPORTS
import numpy as np
import re
from sys import exit

# CLASS DEF


class LightDisplay:
    def __init__(self, lines, dims=(1000, 1000)):
        self.light_grid = np.zeros(dims)
        self.lines = lines

    def process_instructions(self):
        for line in lines:
            fcn, x_inds, y_inds = self.instruct_to_fcn(line)

            # NOTE: to make inclusive, we add one to upper inds
            x_inds[1] += 1
            y_inds[1] += 1

            vals = self.light_grid[x_inds[0]: x_inds[1], y_inds[0]: y_inds[1]]
            mod_vals = []
            for val in vals.flatten():
                mod_vals.append(fcn(val))
            mod_vals = np.array(mod_vals).reshape(vals.shape)  # reshape to 2-D numpy array
            self.light_grid[x_inds[0]: x_inds[1], y_inds[0]: y_inds[1]] = mod_vals

    def print_pretty(self):
        """ right now just print, could do a pretty print w/ shapes/colors"""
        for line in self.light_grid:
            print(''.join(str(int(x)).replace('.', '') for x in list(line)))

    def count_illuminated(self):
        print(f"{int(self.light_grid.sum())} of {int(self.light_grid.shape[0] * self.light_grid.shape[1])} illuminated")


    @staticmethod
    def instruct_to_fcn (instruct_string):
        """ Parse strings to functions to execute on range"""
        # Define dict of fucntions to apply to range
        CMD_FCN_MAP = {
            'turn on': lambda x: 1,
            'turn off': lambda x: 0,
            'toggle': lambda x: abs(x-1),
        }

        fcn = []  # init empty
        for key in CMD_FCN_MAP.keys():
            if key in instruct_string:
                fcn = CMD_FCN_MAP[key]
                break
        if not fcn:
            print(f"ERROR: unknown instruction in {instruct_string}")
            exit(-1)

        # note: format is: "<instruct> <str int> through <str int>"
        # Regex to find numbers
        pat = r'[0-9]*,[0-9]*'
        inds = re.findall(pattern=pat, string=instruct_string) # returns list

        if not inds:
            print(f"ERROR: unknown indices in {instruct_string}")
            exit(-1)

        tmp0 = inds[0].split(",")
        tmp1 = inds[1].split(",")
        x_inds = [int(tmp0[0]), int(tmp1[0])]
        y_inds = [int(tmp0[1]), int(tmp1[1])]

        return fcn, x_inds, y_inds

# MAIN
def main (lines):
    # init class instance:
    light_display = LightDisplay(lines=lines)
    light_display.process_instructions()
    if False:
        light_display.print_pretty()
    light_display.count_illuminated()


if __name__ == '__main__':
    # input here is a simple txt list, wont do anything fancy.
    with open('./inputs/day6_input.txt') as f:
        lines = f.readlines()
    # Strip newlines:
    for i,line in enumerate(lines):
        lines[i] = line.strip('\n')
    f.close()

    main(lines=lines)

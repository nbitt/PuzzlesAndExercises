"""
Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location, and
then an elf at the North Pole calls him via radio and tells him where to move
next. Moves are always exactly one house to the north (^), south (v), east (>),
or west (<). After each move, he delivers another present to the house at his
new location.

However, the elf back at the north pole has had a little too much eggnog, and
so his directions are a little off, and Santa ends up visiting some houses more
than once. How many houses receive at least one present?


-- PART 2:
The next year, to speed up the process, Santa creates a robot version of himself,
Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the
same starting house), then take turns moving based on instructions from the elf,
who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive at least one present?
"""

# IMPORTS
import argparse
from sys import exit
from os import path

# CLASS DEF

class Santa:
    def __init__(self):
        # we will define a coordinate system relative on start location:
        self.position = (0, 0)  # x-y grid, init at 0,0
        self.travel_log = dict()  # dict to hold locs visited. Value is gift count
        self.travel_log[self.position] = 1  # track start location

    def delivery_run (self, flight_path):
        # iterate thru flight path and take appropriate action
        for i, step in enumerate(flight_path):
            if step == "<":
                self.position = (self.position[0] - 1, self.position[1])
            elif step == ">":
                self.position = (self.position[0] + 1, self.position[1])
            elif step == "v":
                self.position = (self.position[0], self.position[1] - 1)
            elif step == "^":
                self.position = (self.position[0], self.position[1] + 1)
            else:
                print(f"ERROR: {step} is an invalid direction!")
                exit(-1)

            # Keep track places visited and gift count
            if self.position in self.travel_log.keys():
                self.travel_log[self.position] += 1  # increment for redundancy
            else:
                self.travel_log[self.position] = 1  # one gift to new loc

    def get_unique_houses(self):
        return len(self.travel_log.keys())

    def get_travel_log(self):
        return self.travel_log

# MAIN


def main (flight_path_fname):
    if path.splitext(flight_path_fname)[-1] != ".txt":
        print(f"ERROR: input {flight_path_fname} is not a .txt file!")
        exit(-1)
    with open(flight_path_fname, "r") as f:  # open txt file for read
        flight_path = f.readlines()[0]

    # instantiate Santa object:
    santa = Santa()

    # Lets FLY!
    santa.delivery_run(flight_path)
    print(f"SOLO SANTA: {santa.get_unique_houses()} houses received >=1 gift")

    # Now part 2 =========
    # make two santas, split instructions
    santa = Santa()  # re-init new santa
    robosanta = Santa()  # init robo santa

    santa.delivery_run(flight_path[0:len(flight_path):2])  # every other
    robosanta.delivery_run(flight_path[1:len(flight_path):2])  # adjascent steps

    combined_locs = list(santa.get_travel_log().keys()) # list of locs for santa 1
    for loc in list(robosanta.get_travel_log().keys()):
        if loc not in combined_locs:
            combined_locs.append(loc)

    print(f"WITH ROBOSANTA: {len(combined_locs)} houses received >=1 gift")


# ENTRY POINT


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AoC Day 2")
    parser.add_argument('--flight_path_fname', type=str, help="name of local .txt file", default="flight_path.txt")
    args = parser.parse_args()
    main(args.flight_path_fname)

"""

The elves are running low on wrapping paper, and so they need to submit an order for more.
They have a list of the dimensions (length l, width w, and height h) of each present, and
only want to order exactly as much as they need.

Fortunately, every present is a box (a perfect right rectangular prism), which makes
calculating the required wrapping paper for each gift a little easier: find the surface
area of the box, which is 2*l*w + 2*w*h + 2*h*l. The elves also need a little extra paper
for each present: the area of the smallest side.

The elves are also running low on ribbon. Ribbon is all the same width, so they only have
to worry about the length they need to order, which they would again like to be exact.

The ribbon required to wrap a present is the shortest distance around its sides, or the
smallest perimeter of any one face. Each present also requires a bow made out of ribbon as
well; the feet of ribbon required for the perfect bow is equal to the cubic feet of volume
of the present. Don't ask how they tie the bow, though; they'll never tell.

"""

# IMPORTS
import argparse
from os import path
from sys import exit


# CLASS DEF

class Present:
    def __init__(self, dimensions):
        self.dimensions = dimensions
        self.l, self.w, self.h = self.split_dimensions()
        self.sq_ft_paper = 0  # init 0
        self.ft_ribbon = 0  # init 0

    def calc_paper_required(self):
        self.sq_ft_paper += self.get_present_surface()
        self.sq_ft_paper += self.get_present_extra_surface()
        return self.sq_ft_paper

    def calc_ribbon_required(self):
        self.ft_ribbon += self.get_smallest_perimeter()
        self.ft_ribbon += self.get_volume()
        return self.ft_ribbon

    def split_dimensions (self):
        # Strip new line, split on x
        dim_split = self.dimensions.strip('\n').split("x")
        if len(dim_split) != 3:
            print(f"ERROR: input {self.dimensions} is not well formed (lxwxh)!")
            exit(-1)

        return int(dim_split[0]), int(dim_split[1]), int(dim_split[2])

    def get_present_surface (self):
        l = self.l
        h = self.h
        w = self.w
        return 2*l*w + 2*w*h + 2*l*h

    def get_present_extra_surface (self):
        sorted_dims = [self.l, self.w, self.h]  # make list for sorting
        sorted_dims.sort()  # sort. default is ascending
        return sorted_dims[0]*sorted_dims[1]  # smallest side

    def get_smallest_perimeter (self):
        sorted_dims = [self.l, self.w, self.h]  # make list for sorting
        sorted_dims.sort()  # sort. default is ascending
        return 2*sorted_dims[0] + 2*sorted_dims[1]  # 2x 2 smallest sides

    def get_volume (self):
        return self.l*self.h*self.w

# MAIN


def main (orders_fname):
    total_sq_footage = 0  # init zero
    total_ribbon = 0  # init zero

    if path.splitext(orders_fname)[-1] != ".txt":
        print(f"ERROR: input {orders_fname} is not a .txt file!")
        exit(-1)
    with open(orders_fname, "r") as f:  # open txt file for read
        orders = f.readlines()

    for order in orders:
        # instantiate class and calc paper needed
        preset = Present(dimensions=order)
        total_sq_footage += preset.calc_paper_required()
        total_ribbon += preset.calc_ribbon_required()

    print(f"Total sq footage needed: {total_sq_footage}")
    print(f"Total ribbon needed (ft): {total_ribbon}")

# ENTRY POINT


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AoC Day 2")
    parser.add_argument('--orders_fname', type=str, help="name of local .txt file", default="orders.txt")
    args = parser.parse_args()
    main(args.orders_fname)
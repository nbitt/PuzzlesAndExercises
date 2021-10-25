"""
Santa is trying to deliver presents in a large apartment building, but he can't
find the right floor - the directions he got are a little confusing. He starts on
the ground floor (floor 0) and then follows the instructions one character at a time.

An opening parenthesis, (, means he should go up one floor, and a closing parenthesis, ),
means he should go down one floor.

The apartment building is very tall, and the basement is very deep; he will never
find the top or bottom floors.

Now, given the same instructions, find the position of the first character that causes
him to enter the basement (floor -1). The first character in the instructions has
position 1, the second character has position 2, and so on.

"""

# IMPORTS
import argparse
import sys

# MAIN


def main (inst):
	# Only allow parens
	if len(inst.replace(")", "").replace("(", "")):
		print("ERROR: must only contain parens ()")
		sys.exit(-1)

	# Instructions indicate that we must go char by char:
	floor = 0  # we start at floor 0
	basement = []
	for i, step in enumerate(inst):
		if step == "(":
			floor += 1  # increment
		elif step == ")":
			floor -= 1  # decrement
		else:
			print(f"ERROR: unknown step instruct: {step}!")
			sys.exit(-1)
		if floor == -1 and not basement:  # hit basement
			basement = i + 1  # per instructions, index starts at 1

	print(f"We've arrived at floor: {floor}")
	if basement:
		print(f"We hit basement at step: {basement}")
	else:
		print(f"We never made it to basement!!")


# ENTRY
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='enter instructions string as single arg',
									 usage='python %(prog)s "<instructions>"')
	parser.add_argument('inst', nargs='+', type=str, help="instructions string")
	args = parser.parse_args()
	main(args.inst[0])

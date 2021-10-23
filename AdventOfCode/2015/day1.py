# Santa is trying to deliver presents in a large apartment building, but he can't 
#find the right floor - the directions he got are a little confusing. He starts on 
#the ground floor (floor 0) and then follows the instructions one character at a time.

# An opening parenthesis, (, means he should go up one floor, and a closing parenthesis, ), 
#means he should go down one floor.

# The apartment building is very tall, and the basement is very deep; he will never 
#find the top or bottom floors.

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
	for step in inst:
		if step == "(":
			floor += 1  # increment
		elif step == ")":
			floor -= 1  # decrement
		else:
			print(f"ERROR: unknown step instruct: {step}!")
			sys.exit(-1)
	print(f"We've arrived at floor: {floor}")


# ENTRY
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='enter instructions string as single arg',
									 usage='python %(prog)s "<instructions>"')
	parser.add_argument('inst', nargs='+', type=str, help="instructions string")
	args = parser.parse_args()
	main(args.inst[0])

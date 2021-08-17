# ========================================
# Overview
# ========================================
#
# Author: nick nesbitt
# 
#
# Summary:
# Exercise created for Recurse Center application.
# Emphasis is placed on keeping program as simple as possible.
#
# Exercise description:
# Write a program that prints out the numbers 1 to 100 (inclusive). 
# If the number is divisible by 3, print Crackle instead of the number. 
# If it's divisible by 5, print Pop. If it's divisible by both 3 and 5, 
# print CracklePop. You can use any language.
#

# ========================================
# Main
# ========================================

def main():
	""" Main function - prints desired output.
		Inputs: none
	"""
	# Inclusive:
	start_val = 1  # start value
	end_val = 100  # ending value
	for i in range(start_val, end_val + 1):
		rem_three = i % 3 # check if 3 is factor
		rem_five = i % 5  # check if 5 is factor

		# Zero remainders indicate divisbility
		if rem_three == 0 and rem_five == 0:
			# divisible by both
			print("CracklePop")
		elif rem_three == 0: 
			print("Crackle")  # divisible by three
		elif rem_five == 0:
			print("Pop")
		else:
			# fallthru
			print(f"{i}")



# ========================================
# Program Entry Point
# ========================================

"""Program Entry Point"""

if __name__ == '__main__':
	main()

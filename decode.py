#!/usr/bin/env python3

# Print the Latin squares encoded by a SAT assignment
# The SAT assignment should be provided on the standard input

import sys

# List of colours
DARK = 2
WHITE = 3

n = 10 # Order of the squares
k = 4 # Number of squares (two colour squares, two symbol squares)

# LS stores the four squares where squares are stored as a list of lists
LS = [[['*' for i in range(n)] for j in range(n)] for l in range(k)]

# Convert a string to an integer if possible; return 0 if not possible
def to_int(str):
	try:
		n = int(str)
		return n
	except ValueError:
		return 0

# Print the symbols in the square A
def print_square(A):
	for i in range(n):
		st = ""
		for j in range(n):
			st += str(A[i][j])+" "
		print(st[:-1])

# Print the colours in the square A
# 'w' denotes white, 'd' denotes dark, and 'l' denotes light
def print_square_colour(A):
	for i in range(n):
		st = ""
		for j in range(n):
			if A[i][j] == WHITE:
				st += "w "
			elif A[i][j] == DARK:
				st += "d "
			else:
				st += "l "
		print(st[:-1])

# Read from the standard input
for line in sys.stdin.readlines():
	if "UNSAT" in line:
		print("UNSAT")
		quit()
	# Get the list of literals in the SAT assignment
	assigns = map(to_int, line.split())
	for assign in assigns:
		# Translate literals into Latin square entries
		vx = (assign-1)%n                  #symbol
		vp = ((assign-1)//n)%n             #column
		vj = (((assign-1)//n)//n)%n        #row
		vi = ((((assign-1)//n)//n)//n)     #square
		# Variables 0001 to 1000 denote the colours of the first square
		# Variables 1001 to 2000 denote the colours of the second square
		# Variables 2001 to 3000 denote the symbols of the first square
		# Variables 3001 to 4000 denote the symbols of the second square
		if assign > 0 and assign <= n*n*n*k:
			assert(LS[vi][vj][vp] == '*')
			LS[vi][vj][vp] = vx
			if vi >= 2 and vx in {0,1,2,3} and vp in {0,1,2,3,4,5}:
				LS[vi-2][vj][vp] = WHITE

# Print squares A and B (colours of squares P and Q)
for p in range(2):
	print_square_colour([[LS[p][i][j] for j in range(n)] for i in range(n)])
	print("")

# Print symbols in squares P and Q
for p in range(2, k):
	print_square([[LS[p][i][j] for j in range(n)] for i in range(n)])
	if p < k-1: print("")

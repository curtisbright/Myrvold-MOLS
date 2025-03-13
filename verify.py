#!/usr/bin/env python3

# Run as ./verify.py VX < sol where sol contains four squares (first two of colours, last two of symbols)

# This script takes from the user four squares of order n=10 from the standard input and the square types on the command-line
# It verifies that
# 1) All colours were assigned a proper symbol for that colour
# 2) The squares are Latin squares that are transversal representations of each other
# 3) There are 2 dark entries in each of the first six columns and the dark entries of the two squares match
# 4) The permutation type of each row is correct for that square type

import sys

# Order of the squares
n = 10

# Read from standard input
# Verify that square names are provided
if len(sys.argv) <= 1:
	print("Need to provide the names of the squares as first command-line argument: e.g. VX")
	quit()

type1 = sys.argv[1][0]
type2 = sys.argv[1][1]
assert(type1 in {'R','S','T','U','V','W','X'})
assert(type2 in {'R','S','T','U','V','W','X'})

# Determine if N is a Latin square
def latin(N):
	for i in range(n):
		if sorted([N[i][j] for j in range(n)]) != list(range(n)):
			return False
	for j in range(n):
		if sorted([N[i][j] for i in range(n)]) != list(range(n)):
			return False
	return True

# Determine if P is a transversal representation of Q
def transversal(P,Q):
	for i in range(n):
		N = []
		for j in range(n):
			for k in range(n):
				if P[i][j] == Q[k][j]:
					N.append(k)
		if sorted(N) != list(range(n)):
			return False
	return True

############################################################################################################
####                                            Square type                                            #####
############################################################################################################
# Colour counts [w1,l1,w2,l2,d] for each row of the seven square types, where:
# w1 is the number of whites in the first six columns
# l1 is the number of lights in the first six columns
# w2 is the number of whites in the last four columns
# l2 is the number of lights in the last four columns
# d is the number of darks (all in the first six columns)
square_data = {
'R': [[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[0,0,4,0,6],[0,0,4,0,6]],
'S': [[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[1,1,3,1,4],[1,1,3,1,4],[1,1,3,1,4]],
'T': [[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[2,2,2,2,2],[1,1,3,1,4],[0,0,4,0,6]],
'U': [[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[2,2,2,2,2],[2,2,2,2,2],[1,1,3,1,4],[1,1,3,1,4]],
'V': [[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[0,0,4,0,6]],
'W': [[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[1,1,3,1,4]],
'X': [[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[3,3,1,3,0],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2],[2,2,2,2,2]]
}
#############################################################

#Read the four matrices to use the data
V1 = [[[0 for k in range(n)] for j in range(n)] for i in range(n)]
X1 = [[[0 for k in range(n)] for j in range(n)] for i in range(n)]
S1 = [[[0 for k in range(n)] for j in range(n)] for i in range(n)]
T1 = [[[0 for k in range(n)] for j in range(n)] for i in range(n)]

# Read from standard input
input_lines = sys.stdin.readlines()

# Read entries of square V1
for i in range(n):
	j = 0
	assert(len(input_lines[i].split()) == n)
	for s in input_lines[i].split():
		assert(s in {"w", "l", "d"})
		V1[i][j] = s
		j += 1

# Read entries of square X1
for i in range(n):
	j = 0
	assert(len(input_lines[n+1+i].split()) == n)
	for s in input_lines[n+1+i].split():
		assert(s in {"w", "l", "d"})
		X1[i][j] = s
		j += 1

# Read entries of square S1
for i in range(n):
	j = 0
	assert(len(input_lines[2*(n+1)+i].split()) == n)
	for s in input_lines[2*(n+1)+i].split():
		assert(int(s) >= 0 and int(s) < n)
		S1[i][j] = int(s)
		j += 1

# Read entries of square T1
for i in range(n):
	j = 0
	assert(len(input_lines[3*(n+1)+i].split()) == n)
	for s in input_lines[3*(n+1)+i].split():
		assert(int(s) >= 0 and int(s) < n)
		T1[i][j] = int(s)
		j += 1

# Verify 1) All colours were assigned a proper symbol for that colour.
for i in range(n):
	for j in range(n):
		if V1[i][j] == 'w':
			assert(S1[i][j] < 4)
		else:
			assert(S1[i][j] >= 4)
		if X1[i][j] == 'w':
			assert(T1[i][j] < 4)
		else:
			assert(T1[i][j] >= 4)

# Verify 2) The squares are Latin squares that are transversal representations of each other.
assert(latin(S1))
assert(latin(T1))
assert(transversal(S1,T1))
assert(transversal(T1,S1))

# Verify 3) There are 2 dark entries in each of the first six columns and the dark entries of the two squares match.
for j in range(6):
	assert([V1[i][j] for i in range(n)].count('d') == 2)
	assert([X1[i][j] for i in range(n)].count('d') == 2)
	assert({S1[i][j] for i in range(n) if V1[i][j] == 'd'} == {T1[i][j] for i in range(n) if X1[i][j] == 'd'})

# Verify 4) The permutation type of each row is correct for that square type.
for i in range(n):
	assert(V1[i][:6].count('w') == square_data[type1][i][0])
	assert(V1[i][:6].count('l') == square_data[type1][i][1])
	assert(V1[i][6:].count('w') == square_data[type1][i][2])
	assert(V1[i][6:].count('l') == square_data[type1][i][3])
	assert(V1[i][:6].count('d') == square_data[type1][i][4])
	assert(V1[i][6:].count('d') == 0)

	assert(X1[i][:6].count('w') == square_data[type2][i][0])
	assert(X1[i][:6].count('l') == square_data[type2][i][1])
	assert(X1[i][6:].count('w') == square_data[type2][i][2])
	assert(X1[i][6:].count('l') == square_data[type2][i][3])
	assert(X1[i][:6].count('d') == square_data[type2][i][4])
	assert(X1[i][6:].count('d') == 0)

print("All constraints verified.")

#!/usr/bin/env python3

# Run as ./verify.py VX < sol where sol contains four squares (first two of colours, last two of symbols)

# This script takes from the user four squares of order n=10 from the standard input and the square types on the command-line
# It verifies that
# 1) All colours were assigned a proper symbol for that colour.
# 2) The squares are Latin squares that are transversal representations of each other.
# 3) There are 2 dark entries in each of the first six columns and the dark entries of the two squares match.
# 4) The permutation type of each row is correct for that square type.
# 5) The coloured transversal representation pair is in normal form (i.e., satisfies the symmetry breaking constraints).
# 6) The 4x4 subsquare consistency constraints are satisfied (using the white entries in the last four columns).

import sys

# Order of the squares
n = 10

use_z4 = "-z4" in sys.argv
if use_z4: sys.argv.remove("-z4")
use_z2xz2 = "-z2xz2" in sys.argv
if use_z2xz2: sys.argv.remove("-z2xz2")
if "-z4z2xz2" in sys.argv: use_z4 = True; use_z2xz2 = True; sys.argv.remove("-z4z2xz2")

# Read from standard input
# Verify that square names are provided
if len(sys.argv) <= 1:
	print("Need to provide the names of the squares as first command-line argument: e.g., VX")
	print("Optionally pass -z4 or -z2xz2 to verify subsquare consistency constraints for Z_4 or Z_2 x Z_2")
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

# Four matrices to store the coloured TRP
Pc = [[[0 for k in range(n)] for j in range(n)] for i in range(n)]
Qc = [[[0 for k in range(n)] for j in range(n)] for i in range(n)]
P = [[[0 for k in range(n)] for j in range(n)] for i in range(n)]
Q = [[[0 for k in range(n)] for j in range(n)] for i in range(n)]

# Read from standard input
input_lines = sys.stdin.readlines()

# Read colours of square P
for i in range(n):
	j = 0
	assert(len(input_lines[i].split()) == n)
	for s in input_lines[i].split():
		assert(s in {"w", "l", "d"})
		Pc[i][j] = s
		j += 1

# Read colours of square Q
for i in range(n):
	j = 0
	assert(len(input_lines[n+1+i].split()) == n)
	for s in input_lines[n+1+i].split():
		assert(s in {"w", "l", "d"})
		Qc[i][j] = s
		j += 1

# Read symbols of square P
for i in range(n):
	j = 0
	assert(len(input_lines[2*(n+1)+i].split()) == n)
	for s in input_lines[2*(n+1)+i].split():
		assert(int(s) >= 0 and int(s) < n)
		P[i][j] = int(s)
		j += 1

# Read symbols of square Q
for i in range(n):
	j = 0
	assert(len(input_lines[3*(n+1)+i].split()) == n)
	for s in input_lines[3*(n+1)+i].split():
		assert(int(s) >= 0 and int(s) < n)
		Q[i][j] = int(s)
		j += 1

# Verify 1) All colours were assigned a proper symbol for that colour.
for i in range(n):
	for j in range(n):
		if Pc[i][j] == 'w':
			assert(P[i][j] < 4)
		else:
			assert(P[i][j] >= 4)
		if Qc[i][j] == 'w':
			assert(Q[i][j] < 4)
		else:
			assert(Q[i][j] >= 4)

# Verify 2) The squares are Latin squares that are transversal representations of each other.
assert(latin(P))
assert(latin(Q))
assert(transversal(P,Q))
assert(transversal(Q,P))

# Verify 3) There are 2 dark entries in each of the first six columns and the dark entries of the two squares match.
for j in range(6):
	assert([Pc[i][j] for i in range(n)].count('d') == 2)
	assert([Qc[i][j] for i in range(n)].count('d') == 2)
	assert({P[i][j] for i in range(n) if Pc[i][j] == 'd'} == {Q[i][j] for i in range(n) if Qc[i][j] == 'd'})

# Verify 4) The permutation type of each row is correct for that square type.
for i in range(n):
	assert(Pc[i][:6].count('w') == square_data[type1][i][0])
	assert(Pc[i][:6].count('l') == square_data[type1][i][1])
	assert(Pc[i][6:].count('w') == square_data[type1][i][2])
	assert(Pc[i][6:].count('l') == square_data[type1][i][3])
	assert(Pc[i][:6].count('d') == square_data[type1][i][4])
	assert(Pc[i][6:].count('d') == 0)

	assert(Qc[i][:6].count('w') == square_data[type2][i][0])
	assert(Qc[i][:6].count('l') == square_data[type2][i][1])
	assert(Qc[i][6:].count('w') == square_data[type2][i][2])
	assert(Qc[i][6:].count('l') == square_data[type2][i][3])
	assert(Qc[i][:6].count('d') == square_data[type2][i][4])
	assert(Qc[i][6:].count('d') == 0)

# Verify 5) The symmetry breaking
# The rows of the same transversal types are lexicographically sorted in both squares
for i in range(n-1):
	if square_data[type1][i] == square_data[type1][i+1]:
		assert(P[i][0] < P[i+1][0])
	if square_data[type2][i] == square_data[type2][i+1]:
		assert(Q[i][0] < Q[i+1][0])
# First row of first square is in normal form
assert(P[0] == [0, 1, 2, 4, 5, 6, 3, 7, 8, 9] or P[0] == [0, 1, 3, 4, 5, 6, 2, 7, 8, 9] or P[0] == [0, 2, 3, 4, 5, 6, 1, 7, 8, 9])

# Verify 6) The subsquare consistency constraints
Ls = [[[0,1,2,3],[1,2,3,0],[2,3,0,1],[3,0,1,2]],
      [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]]
compatible_with_subsq = [True, True]
for subsq in range(2):
	L = Ls[subsq]
	for i in range(n):
		for j in range(6,n):
			for jp in range(j+1,n):
				for k in range(4):
					if P[i][j] == L[k][j-6] and P[i][jp] == L[k][jp-6]: compatible_with_subsq[subsq] = False
					if Q[i][j] == L[k][j-6] and Q[i][jp] == L[k][jp-6]: compatible_with_subsq[subsq] = False
	if compatible_with_subsq[subsq]:
		print(f"TRP is compatible with 4x4 Latin subsquare Omega_{subsq+1}" + (" (Cayley table of Z_4)" if subsq == 0 else " (Cayley table of Z_2xZ_2)"))
assert(compatible_with_subsq != [False, False])
if use_z4: assert(compatible_with_subsq[0])
if use_z2xz2: assert(compatible_with_subsq[1])

print("All constraints verified.")

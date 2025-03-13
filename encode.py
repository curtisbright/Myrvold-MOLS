#!/usr/bin/env python3
import sys

# Colour constants
DARK = 2
WHITE = 3

# Order of the squares
n = 10

# Transversal type data for the square types
# The ith entry of each list represents that row i has form p_i (has i whites in the last 4 columns)
transversal_types = {
'R': 8*[1] + 2*[4],
'S': 7*[1] + 3*[3],
'T': 7*[1] + [2] + [3] + [4],
'U': 6*[1] + 2*[2] + 2*[3],
'V': 6*[1] + 3*[2] + [4],
'W': 5*[1] + 4*[2] + [3],
'X': 4*[1] + 6*[2]
}

# Verify that square names are provided
if len(sys.argv) <= 1 or len(sys.argv[1]) <= 1:
	print("Need to provide the names of the squares as first command-line argument: e.g. VX")
	quit()

# Verify the square types are valid
P_type = sys.argv[1][0]
Q_type = sys.argv[1][1]

if not P_type in ['R','S','T','U','V','W','X']:
	print("Incorrect first square type. Type must be one of {R,S,T,U,V,W,X}.")
	quit()

if not Q_type in ['R','S','T','U','V','W','X']:
	print("Incorrect second square type. Type must be one of {R,S,T,U,V,W,X}.")
	quit()

# Multi-dimensional arrays to hold the variables used in the encoding
Pc = [[[0 for k in range(n)] for j in range(n)] for i in range(n)] # Colours of square P
Qc = [[[0 for k in range(n)] for j in range(n)] for i in range(n)] # Colours of square Q
P = [[[0 for k in range(n)] for j in range(n)] for i in range(n)] # Symbols of square P
Q = [[[0 for k in range(n)] for j in range(n)] for i in range(n)] # Symbols of square Q
Z = [[[0 for k in range(n)] for j in range(n)] for i in range(n)] # Witness square ensuring (P,Q) is a transversal representation pair

# Counter for # of variables used in SAT instance
total_vars = 0
# List to hold clauses of SAT instance
clauses = []

# Generate a clause containing the literals in the set X
def generate_clause(X):
	clause = ""
	for x in X:
		clause += str(x) + " "
	clauses.append(clause + "0")

# Generate a clause specifying (x1 & ... & xn) -> (y1 | ... | yk) where X = {x1, ..., xn} and Y = {y1, ..., yk}
def generate_implication_clause(X, Y):
	if 'F' in X or 'T' in Y:
		return
	while 'T' in X: X.remove('T')
	while 'F' in Y: Y.remove('F')
	clause = ""
	for x in X:
		clause += str(-x) + " "
	for y in Y:
		clause += str(y) + " "
	clauses.append(clause + "0")

# Generate clauses encoding exactly one variable in X is assigned true
def generate_exactly_one_clauses(X):
	generate_adder_clauses(X, 1, 1)

# Return the number of leaves under node k in the complete binary tree with N nodes
def num_leaves_under(N, k):
	if k >= N: return 0
	if 2*k+1 >= N: return 1
	return num_leaves_under(N, 2*k+1) + num_leaves_under(N, 2*k+2)

# Generate clauses encoding that <= s variables and >= l variables in X are assigned true using the totalizer encoding
def generate_adder_clauses(X, l, s):
	global total_vars

	n = len(X)
	# Totalizer auxiliary variables
	R = [['F' for j in range(n+2)] for i in range(2*n-1)]
	for i in range(2*n-1):
		R[i][0] = 'T'

	for i in range(n-1):
		t = num_leaves_under(2*n-1, i)
		for j in range(t):
			total_vars += 1
			R[i][j+1] = total_vars
	for i in range(n-1, 2*n-1):
		R[i][1] = X[i-n+1]

	for i in range(n-1):
		m = num_leaves_under(2*n-1, i)
		for sigma in range(m+1):
			# Solve alpha + beta = sigma
			for alpha in range(sigma+1):
				beta = sigma - alpha
				generate_implication_clause({R[2*i+1][alpha], R[2*i+2][beta]}, {R[i][sigma]})
				generate_implication_clause({R[i][sigma+1]}, {R[2*i+1][alpha+1], R[2*i+2][beta+1]})

	for i in range(1,l+1):
		generate_clause({R[0][i]})
	for i in range(s+1,n+1):
		generate_clause({-R[0][i]})

# Define colour variables for P
for i in range(n):
	for j in range(n):
		for k in range(n):
			total_vars += 1
			Pc[i][j][k] = total_vars

# Define colour variables for Q
for i in range(n):
	for j in range(n):
		for k in range(n):
			total_vars += 1
			Qc[i][j][k] = total_vars

# Define symbol variables for P
for i in range(n):
	for j in range(n):
		for k in range(n):
			total_vars += 1
			P[i][j][k] = total_vars

# Define symbol variables for Q
for i in range(n):
	for j in range(n):
		for k in range(n):
			total_vars += 1
			Q[i][j][k] = total_vars

# Define symbol variables for Z
for i in range(n):
	for j in range(n):
		for k in range(n):
			total_vars += 1
			Z[i][j][k] = total_vars

# Constraints ensuring that Q = PZ
for i in range(n):
	for j in range(n):
		for k in range(n):
			for ip in range(n):
				generate_implication_clause({P[i][j][k], Q[ip][j][k]}, {Z[ip][j][i]})
				generate_implication_clause({P[i][j][k], Z[ip][j][i]}, {Q[ip][j][k]})
				generate_implication_clause({Z[ip][j][i], Q[ip][j][k]}, {P[i][j][k]})

# Z must be a Latin square
for i in range(n):
	for j in range(n):
		generate_exactly_one_clauses([Z[i][k][j] for k in range(n)])
		generate_exactly_one_clauses([Z[i][j][k] for k in range(n)])
		generate_exactly_one_clauses([Z[k][i][j] for k in range(n)])

# Generate constraints encoding that every row of the square A has colours matching the list of transversal types in M
def colour_constraints(M, A):
	for i in range(n):
		# Row i is of form p_i, so ensure there are M[i] white entries in the last four columns of row i
		generate_adder_clauses([A[i][j][WHITE] for j in range(6,n)], M[i], M[i])
		# Row i is of form p_i, so ensure there are 2*M[i]-2 dark entries in the first six columns of row i
		generate_adder_clauses([A[i][j][DARK] for j in range(6)], 2*M[i]-2, 2*M[i]-2)

colour_constraints(transversal_types[P_type], Pc)
colour_constraints(transversal_types[Q_type], Qc)

# Two darks per column in P
for j in range(6):
	generate_adder_clauses([Pc[i][j][DARK] for i in range(n)], 2, 2)

# Two darks per column in Q
for j in range(6):
	generate_adder_clauses([Qc[i][j][DARK] for i in range(n)], 2, 2)

# Set all extraneous variables to false
for i in range(n):
	for j in range(n):
		for k in range(n):
			if not k in {WHITE, DARK}:
				generate_clause({-Pc[i][j][k]})
				generate_clause({-Qc[i][j][k]})
	for j in range(6, n):
		generate_clause({-Pc[i][j][DARK]})
		generate_clause({-Qc[i][j][DARK]})
	for j in range(6):
		generate_clause({-Pc[i][j][WHITE]})
		generate_clause({-Qc[i][j][WHITE]})

# Symbol to colour correspondence:

for i in range(n):
	for j in range(6, n):
		for k in range(4):
			generate_implication_clause({P[i][j][k]}, {Pc[i][j][WHITE]})

for i in range(n):
	for j in range(6, n):
		for k in range(4):
			generate_implication_clause({Q[i][j][k]}, {Qc[i][j][WHITE]})

# Colour to symbol correspondence:

for i in range(n):
	for j in range(6, n):
		generate_implication_clause({Pc[i][j][WHITE]}, {P[i][j][0], P[i][j][1], P[i][j][2], P[i][j][3]})
	for j in range(6):
		generate_implication_clause({Pc[i][j][DARK]}, {P[i][j][4], P[i][j][5], P[i][j][6], P[i][j][7], P[i][j][8], P[i][j][9]})

for i in range(n):
	for j in range(6, n):
		generate_implication_clause({Qc[i][j][WHITE]}, {Q[i][j][0], Q[i][j][1], Q[i][j][2], Q[i][j][3]})
	for j in range(6):
		generate_implication_clause({Qc[i][j][DARK]}, {Q[i][j][4], Q[i][j][5], Q[i][j][6], Q[i][j][7], Q[i][j][8], Q[i][j][9]})

# Fixing the entries of the last row of P

if P_type in ['R', 'T', 'V']:
	# Final row is [4,5,6,7,8,9,0,1,2,3]
	L = [P[9][0][4], P[9][1][5], P[9][2][6], P[9][3][7], P[9][4][8], P[9][5][9], P[9][6][0], P[9][7][1], P[9][8][2], P[9][9][3]]
	for i in L:
		generate_clause([i])
	for i in range(6):
		generate_clause([Pc[9][i][DARK]])

if P_type in ['S', 'U', 'W']:
	# Final row is [3,4,5,6,7,8,0,1,2,9]
	L = [P[9][0][3], P[9][1][4], P[9][2][5], P[9][3][6], P[9][4][7], P[9][5][8], P[9][6][0], P[9][7][1], P[9][8][2], P[9][9][9]]
	for i in L:
		generate_clause([i])
	for i in range(2, 6):
		generate_clause([Pc[9][i][DARK]])

if P_type == 'X':
	# Final row is [2,3,4,5,6,7,0,1,8,9]
	L = [P[9][0][2], P[9][1][3], P[9][2][4], P[9][3][5], P[9][4][6], P[9][5][7], P[9][6][0], P[9][7][1], P[9][8][8], P[9][9][9]]
	for i in L:
		generate_clause([i])
	for i in range(4, 6):
		generate_clause([Pc[9][i][DARK]])

# Ensure consistency of the dark entries in P and Q
for i in range(n):
	for j in range(6):
		for l in range(n):
			for k in range(n):
				generate_implication_clause({Qc[i][j][DARK], Q[i][j][k], P[l][j][k]}, {Pc[l][j][DARK]})
				generate_implication_clause({Pc[l][j][DARK], Q[i][j][k], P[l][j][k]}, {Qc[i][j][DARK]})

# Latin square constraints for P and Q
for i in range(n):
	for j in range(n):
		generate_exactly_one_clauses([P[i][j][k] for k in range(n)])
		generate_exactly_one_clauses([Q[i][j][k] for k in range(n)])
		generate_exactly_one_clauses([P[i][k][j] for k in range(n)])
		generate_exactly_one_clauses([Q[i][k][j] for k in range(n)])
		generate_exactly_one_clauses([P[k][j][i] for k in range(n)])
		generate_exactly_one_clauses([Q[k][j][i] for k in range(n)])

# Order rows of P and Q of the same type lexicographically

# Generate symbol ordering constraints within a block of the same colour
# K is the list of transversal types for the square H; sort_final_row controls if the final row of H should also be sorted
def lex_order(K, H, sort_final_row):
	for i in range(n-1 if sort_final_row else n-2):
		if K[i] == K[i+1]:
			for k in range(n):
				for l in range(k):
					generate_implication_clause({H[i][0][k]}, {-H[i+1][0][l]})

lex_order(transversal_types[P_type], P, False) # Final row of P is not sorted as its entries were already fixed
lex_order(transversal_types[Q_type], Q, True)

# Output SAT instance in DIMACS format
print("p cnf {} {}".format(total_vars, len(clauses)))
for clause in clauses:
	print(clause)

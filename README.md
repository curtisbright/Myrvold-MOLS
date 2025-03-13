# Scripts accompanying "Myrvold's Results on Orthogonal Triples of 10 × 10 Latin Squares: A SAT Investigation"

## Overview

This repository contains scripts for a SAT investigation into Myrvold's results on orthogonal triples of 10 × 10 Latin squares.

In 1999, Myrvold showed that there are 28 possibilities for a pair of orthogonal Latin squares where both Latin squares are orthogonal to a third Latin square having a 4 × 4 Latin subsquare.  She eliminated 20 of those cases from consideration and left open the remaining 8 cases.  The scripts in this repository can be used to verify Myrvold's results and find Latin square pairs for the remaining 8 cases.

### Execution
- **`run.sh`**: Executes the SAT solving workflow:
  1. Generates a CNF encoding using the script `encode.py`.
  2. Runs the SAT solver Kissat on the CNF encoding.  (Kissat is first downloaded and compiled using the script `compile-kissat.sh` if it is not already present.)
  3. If a solution was found, it is converted into a pair of Latin squares using the script `decode.py`.
  4. Finally, it is verified that the Latin squares satisfy the expected properties using the script `verify.py`.
  5. The Kissat solving log is saved in the `log` subdirectory.
- **`summary.sh`**: Prints a table summarizing the results from the log files.  (Requires the program `datamash` to be installed.)

### Example

Myrvold's eight remaining cases are named SX, UX, VX, WX, XX, UU, UW, and WW.  The script `run.sh` takes the case to solve as a single command-line argument.  For example, to solve the case UU:

```./run.sh UU```

## References

Myrvold, W.: Negative results for orthogonal triples of Latin squares of order 10.  Journal of Combinatorial Mathematics and Combinatorial Computing 29, 95–106
(1999)

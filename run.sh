#!/bin/bash

solver="./kissat/build/kissat"

# Check for subsquare consistency option -z4 or -z2xz2, -t with timeout, or -s with seed
while getopts "z:t:s:" opt; do
	case "$opt" in
		z) subsq="-z$OPTARG" ;;
		t) timeout=" --time=$OPTARG" ;;
		s) seed="$OPTARG" ;;
	esac
done
shift $((OPTIND-1))

# Ensure pair type given on command-line
if [ -z $1 ]
then
	echo "Usage: $0 [-z4|-z2xz2] [-t timeout] [-s seed] Pair_Type (e.g., VX)"
	echo "Pass -z4 to enforce subsquare consistency with Z_4; pass -z2xz2 to enforce subsquare consistency with Z_2 x Z_2"
	echo "Pass -t timeout to stop solving after timeout seconds"
	echo "Pass -s seed to set the random seed of the solver"
	exit 1
fi

case=$1
if [[ ! $case =~ ^[RSTUVWX][RSTUVWX] ]]
then
	echo "Invalid square type. Both square types must be one of {R,S,T,U,V,W,X}."
	exit 1
fi

# Ensure Kissat solver is compiled in kissat directory
if [ ! -f $solver ]
then
	./compile-kissat.sh
fi

mkdir -p log # Directory to store log of solver output

if [ -z $seed ]
then
	seed=$(shuf -i 0-999999999 -n 1)
fi

logname=$case$subsq-$seed

command="./encode.py $subsq $case | $solver$timeout --seed=$seed | tee log/$logname.log"
echo $command
eval $command

if grep -q "s SATISFIABLE" log/$logname.log
then
	# Verify the found solution satisfies the expected properties
	grep '^v' log/$logname.log | ./decode.py | ./verify.py $subsq $case
else
	grep "s UNSATISFIABLE" log/$logname.log
fi

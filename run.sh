#!/bin/bash

solver="./kissat/build/kissat"

# Ensure pair type given on command-line
if [ -z $1 ]
then
	./encode.py
	exit 1
fi

if [[ ! $1 =~ ^[RSTUVWX][RSTUVWX] ]]
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

seed=$(shuf -i 0-999999999 -n 1)

logname=$1-$(date +%Y-%m-%d)-$seed

command="./encode.py $1 | $solver --seed=$seed | tee log/$logname.log"
echo $command
eval $command

if grep -q "s SATISFIABLE" log/$logname.log
then
	# Verify the found solution satisfies the expected properties
	grep '^v' log/$logname.log | ./decode.py | ./verify.py $1
else
	grep "s UNSATISFIABLE" log/$logname.log
fi

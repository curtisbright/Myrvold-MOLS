#!/bin/bash

# Script to summarize the results of the logs (requires the program datamash)
# Call with -l for LaTeX table output

# Check if datamash exists
if ! command -v datamash &> /dev/null
then
	echo "Error: This script requires the program datamash to be installed; exiting."
	exit
fi

shopt -s extglob

while getopts "l" opt
do
	case "$opt" in
		l) sep=" &"; endl=" \\\\" ;;
	esac
done
shift $((OPTIND-1))

stats=(count mean median min max)
types=(UU SX UW WW VX UX WX XX)
subsqs=("" "-z4" "-z2xz2" "-z4z2xz2")

printf "%-12s%s" "pair type" "$sep"

for stat in ${stats[@]}
do
	printf "%11s%s" $stat "$sep"
done

printf "%s\n" "$endl"

for subsq in "${subsqs[@]}"
do
	for type in ${types[@]}
	do
		logs=log/$type$subsq-+([0-9]).log
		if ! ls $logs 1> /dev/null 2>&1
		then
			continue
		else
			c=$(ls $logs -l | wc -l)
		fi
		printf "%-12s%s" $type$subsq "$sep"
		for stat in ${stats[@]}
		do
			if grep -l -L "s UNKNOWN" $logs | xargs grep -q "c process-time" 2>/dev/null
			then
				st=$(grep -l -L "s UNKNOWN" $logs | xargs grep "c process-time" | rev | cut -d' ' -f2 | rev)

				# Consider timeouts in all calculations except for count
				if [ $stat != "count" ]
				then
					# Treat a timeout as a running time of one week
					while (( $(wc -w <<< $st) < $c ))
					do
						st+=$'\n'604800
					done
				fi
				t=$(datamash $stat 1 <<< $st)
				if [ $t == "604800" ]
				then
					t="timeout"
				elif [ $stat != "count" ]
				then
					t=$(printf "%.1f" "$t")
				fi
			else
				# No log files of the given type
				t=0
				if [ $stat != "count" ]
				then
					t="-"
				fi
			fi
			if [ $stat != "count" ]
			then
				printf "%11s%s" "$t" "$sep"
			else
				printf "%8d/%2d%s" $t $c "$sep"
			fi
		done
		printf "%s\n" "$endl"
	done
done

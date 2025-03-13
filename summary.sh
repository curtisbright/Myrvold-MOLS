#!/bin/bash

shopt -s extglob

# Script to summarize the results of the logs (requires the program datamash)

stats=(count mean median min max)
types=(SX UX VX WX XX UU UW WW)

printf "%2s" ""

for stat in ${stats[@]}
do
	printf "%11s" $stat
done

printf "\n"

for type in ${types[@]}
do
	logs=log/$type-+([0-9])-+([0-9])-+([0-9])-+([0-9]).log
	if ! ls $logs 1> /dev/null 2>&1
	then
		continue
	else
		c=$(ls $logs -l | wc -l)
	fi
	printf "%2s" $type
	for stat in ${stats[@]}
	do
		if grep -q "c process-time" $logs 2>/dev/null
		then
			st=$(grep "c process-time" $logs | rev | cut -d' ' -f2 | rev)

			# Consider timeouts in all calculations except for count
			if [ $stat != "count" ]
			then
				# Treat a timeout as a running time of two weeks
				while (( $(wc -w <<< $st) < $c ))
				do
					st+=$'\n'1209600
				done
			fi
			t=$(datamash $stat 1 <<< $st)
			if [ $t == "1209600" ]
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
			printf "%11s" "$t"
		else
			printf "%8d/%2d" $t $c
		fi
	done
	printf "\n"
done

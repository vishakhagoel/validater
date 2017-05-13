#!/bin/bash

# read all testcases from file given as argument to run the script
while read -r line || [[ -n "$line" ]]; do

	var=$((var+1))
    echo "Testcase $var: $line"

    # run python script and store output
	output=$($line)  	
    echo "Output: $output"

    # read expected output from file and compare with $output
    read -r line || [[ -n "$line" ]]
    if [ "$output" == "$line" ]
    then
    	echo "Result: Pass"
    else
    	echo "Result: Failed"
    fi

    echo -e "\n"
done < "$1"
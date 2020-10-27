#!/bin/bash   

OUTPUT="./test-results.txt"
COMM="python3 solve_sudoku.py"

# start with a new file
rm ${OUTPUT}      

for file in *.cnf ; do 
    echo -e "\n----------------------------------------------------------------------------------\n" >> ${OUTPUT} 
    echo -e "\t\t\t\tFile: ${file}\n\n" >> ${OUTPUT} 
    for threshold in 0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0 ; do 
        ${COMM} ${file} -g ${threshold} >> ${OUTPUT}                                          
        ${COMM} ${file} ${threshold} >> ${OUTPUT} 
    done
done
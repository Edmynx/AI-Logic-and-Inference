from display import display_sudoku_solution
import random, sys, time
from SAT import SAT
from GSAT import GSAT


if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    random.seed(1)

    puzzle_name = str(sys.argv[1][:-4])
    sol_filename = puzzle_name + ".sol"

    # execute the test with GSAT if the "-g" option is specified at the command line

    print("\n--------------------\n")
    if len(sys.argv) >= 2 and sys.argv[2] == "-g":
        print("Running test with GSAT:\n")
        print("\tOn the file:", sys.argv[1])
        sat = GSAT(sys.argv[1])

        if len(sys.argv) > 3:
            sat.h = float(sys.argv[3])
            print("With the threshold value:", sys.argv[3])

    # otherwise assume that the test has to be run with SAT
    else:
        print("Running test with SAT:\n")
        print("On the file:", sys.argv[1])
        sat = GSAT(sys.argv[1])

        if len(sys.argv) > 2:
            sat.h = float(sys.argv[2])
            print("With the threshold value:", sys.argv[2])

    time1 = time.time()
    result = sat.walksat()
    time2 = time.time()

    time_result = time2 - time1

    print("Runtime for walksat in seconds:", time_result, "\n")

    if result:
        sat.write_solution(sol_filename)
        print("Result:")
        display_sudoku_solution(sol_filename)
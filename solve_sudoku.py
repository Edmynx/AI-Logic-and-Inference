from display import display_sudoku_solution
import random, sys
from SAT import SAT
from GSAT import GSAT

if __name__ == "__main__":
    # for testing, always initialize the pseudorandom number generator to output the same sequence
    #  of values:
    #random.seed()

    puzzle_name = str("one_cell.cnf")
    sol_filename = puzzle_name + ".sol"

    sys.stdout.write(sol_filename)

    sat = SAT("one_cell.cnf")

    result = sat.walksat()

    if result:
        sat.write_solution(sol_filename)
        display_sudoku_solution(sol_filename)
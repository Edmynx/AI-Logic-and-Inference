import random, sys

sys.setrecursionlimit(10**6)

class GSAT():
    def __init__(self, cnf_file, h=1):
        self.h = h  # threshold value for randomly selecting variables
        self.var_map = {}  # maps clause literals in the given file to integer variables
        self.model = None  # model for assigning values to integer variables
        self.clauses = []  # list of all clauses in the given file
        self.var_clauses = {}
        self.__convert_to_generic_SAT__(cnf_file)  # do SAT conversion

    # convert every unique clause literal in the given cnf_file
    # to an integer that can be used for generic SAT operations
    def __convert_to_generic_SAT__(self, cnf_file):
        var_count = 0
        file_read = open(cnf_file, "r")
        for cnf in file_read:
            clause = set()
            for cnf_literal in cnf.split():
                neg = False
                if cnf_literal[0] == "-":
                    neg = True
                    cnf_literal = cnf_literal[1:]

                # make sure the variable has not been added already
                if cnf_literal not in self.var_map.keys():
                    var_count += 1
                    self.var_map[cnf_literal] = var_count
                    # since the var hasn't been seen yet, it mustn't belong to any clause yet
                    # so create a space for it in the var_clauses map
                    self.var_clauses[var_count] = []  # will store a set (list better, set can't be hashed into set)
                clause.add((-self.var_map[cnf_literal] if neg else self.var_map[cnf_literal]))
                # let var point to clause (tells us var belongs to the clause)
                # used later to check if a var belongs to a given clause
                self.var_clauses.get(self.var_map[cnf_literal]).append(clause)
            self.clauses.append(clause)

        self.model = [random.getrandbits(1) for i in range(var_count)]
        file_read.close()

    def write_solution(self, filename):
        file_write = open(filename, "w")
        for cnf_literal, value in sorted(self.var_map.items(), key=lambda items: items[1]):
            file_write.write(("-" if not self.model[value - 1] else "") + cnf_literal + "\n")
        file_write.close()

    # check if current model satisfies the given clause
    def __is_clause_satisfied__(self, clause):
        # select a variable (var) and check if the selected var
        # satisfies the given clause
        # given a var i, the var index in the model is i - 1
        for var in clause:
            if self.model[abs(var) - 1] == (0 if var < 0 else 1):
                return 1 # once the clause has been satisfied, there's no need to keep searching
        return 0

    def __are_all_clauses_satisfied__(self):
        clauses_satisfied = 0
        for i in range(len(self.clauses)):
            result = self.__is_clause_satisfied__(self.clauses[i])
            if result:
                clauses_satisfied += result
            else:
                return 0

        return clauses_satisfied == len(self.clauses)

    def walksat(self):
        # check if the current assignment satisfies all the clauses
        # return 1 (success) if it does

        if self.__are_all_clauses_satisfied__():
            return 1

        # pick a number between 0 and 1
        # if the number > the threshold value, choose a
        # variable uniformly at random and flip its value
        if random.uniform(0, 1) >= self.h:
            random_var_index = random.randint(0, len(self.model) - 1)
            self.model[random_var_index] = int(not self.model[random_var_index])

        else:
            # for each variable (var), score how many clauses
            # would be satisfied if the var's value were flipped
            score_map = {}
            for i in range(len(self.model)):
                self.model[i] = int(not self.model[i])  # temporarily flip var's value
                var_score_satisfied = 0  # how many clauses would be satisfied?
                # go through every clause the var is in and check for satisfaction
                # var index is i but the var is i + 1 instead
                for clause in self.var_clauses[i + 1]:
                    var_score_satisfied += self.__is_clause_satisfied__(clause)
                score_map[i] = var_score_satisfied  # hash each var's score into a map using its index (i)
                self.model[i] = int(not self.model[i])  # un-flip var's value

            # uniformly at random choose one of the vars with
            # the highest score and flip it's value
            # note that variable's index was stored
            # this can be used to access the model directly
            max_score = max(score_map.values())
            max_var_indices = [key for key, value in filter(lambda items: items[1] == max_score, score_map.items())]
            max_index_random = random.choice(max_var_indices)
            self.model[max_index_random] = int(not self.model[max_index_random])

        return self.walksat()  # repeat the walksat process recursively




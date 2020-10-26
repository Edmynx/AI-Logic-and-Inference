import random

class GSAT():
    def __init__(self, cnf_file, h=0.3):
        self.h = h  # threshold value for randomly selecting variables
        self.var_map = {}  # maps clause literals in the given file to integer variables
        self.model = None  # model for assigning values to integer variables
        self.clauses = []  # list of all clauses in the given file
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

                if (-self.var_map[cnf_literal] if neg else self.var_map[cnf_literal]) not in clause:
                    clause.add((-self.var_map[cnf_literal] if neg else self.var_map[cnf_literal]))
            self.clauses.append(clause)
        self.model = [random.getrandbits(1) for i in range(var_count)]
        file_read.close()

    def write_solution(self, filename):
        file_write = open(filename, "w")
        for cnf_literal, value in sorted(self.var_map.items(), key=lambda items: items[1]):
            print("hhhhhaihfhehf", cnf_literal, value)
            file_write.write(("-" if not self.model[value - 1] else "") + cnf_literal + "\n")
        file_write.close()

    # check if current model satisfies all the clauses
    def __is_satisfied__(self, clause):
        satisfied = set()  # clauses that have been satisfied
        print("\n\n\ncurrent-mod", self.model)
        # for every clause known
        for i in range(len(self.clauses)):
            print("\nclauses len", len(self.clauses), self.clauses[i], "current", i)
            print("current-mod", self.model)
            for var in self.clauses[i]:
                print("var", var)
                # check if the variable (var) satisfies the given clause
                # given a var i, the var index in the model is i - 1
                if self.model[abs(var) - 1] == (0 if var < 0 else 1):
                    satisfied.add(i)
                    print("satisfied", satisfied)
                    break # once the clause has been satisfied, there's no need to keep searching

        return len(satisfied) == len(self.clauses)

    def walksat(self):
        # check if the current assignment satisfies all the clauses
        # return 1 (success) if it does
        if self.__is_satisfied__():
            print("SATISFIED.......")
            return 1

        # pick a number between 0 and 1
        a = random.uniform(0, 1)
        print("prob", a)
        # if the number > the threshold value, choose a
        # variable uniformly at random and flip its value
        if a >= self.h:
            print("prob", a)
            random_var_index = random.randint(0, len(self.model) - 1)
            print("if random index", random_var_index)
            self.model[random_var_index] = int(not self.model[random_var_index])

            self.walksat()  # repeat the walksat process recursively

        else:
            # for each variable (var), score how many clauses
            # would be satisfied if the var's value were flipped
            score_map = {}
            for i in range(len(self.model)):
                var_flipped_val = int(not self.model[i])
                var_score_satisfied = 0  # how many clauses would be satisfied?
                for clause in self.clauses:
                    # check if the var at index i in the model is in the clause
                    # var index is i but the var is i + 1 instead
                    for clause_var in clause:
                        if i + 1 == abs(clause_var):
                            # check if clause is satisfied with its flipped value
                            if var_flipped_val == (0 if clause_var < 0 else 1):
                                var_score_satisfied += 1
                                break  # once the var has been satisfied, there's no need to keep searching
                score_map[i] = var_score_satisfied # hash each var's score into a map using its index (i)

            # uniformly at random choose one of the vars with
            # the highest score and flip it's value
            # note that variable's index was stored
            # this can be used to access the model directly
            max_score = max(score_map.values())
            print("max score..........", max_score)
            max_vars = [key for key, value in filter(lambda items: items[1] == max_score, score_map.items())]
            print("selected high vars", max_vars)
            max_index_random = random.choice(max_vars)
            print("max_index_ran", max_index_random)
            self.model[max_index_random] = int(not self.model[max_index_random])

            self.walksat()  # repeat the walksat process recursively

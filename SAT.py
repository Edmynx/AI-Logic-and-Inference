import random

from GSAT import GSAT

class SAT(GSAT):
    def __init__(self, cnf_file, p=1, max_flips=100000):
        GSAT.__init__(self, cnf_file, p)
        self.max_flips = max_flips
        self.satisfied = set()  # clauses that have been satisfied at present

    # check if current model satisfies all the clauses
    def __are_all_clauses_satisfied__(self):
        self.satisfied = set()
        for i in range(len(self.clauses)):
            if i not in self.satisfied:
                if self.__is_clause_satisfied__(self.clauses[i]):
                    self.satisfied.add(i)
        return len(self.satisfied) == len(self.clauses)

    def walksat(self):
        for i in range(self.max_flips):
            if self.__are_all_clauses_satisfied__():
                return 1

            random_clause_index = random.randint(0, len(self.clauses) - 1)
            while random_clause_index in self.satisfied:
                random_clause_index = random.randint(0, len(self.clauses) - 1)

            if random.uniform(0, 1) >= self.h:
                random_var = random.choice(tuple(self.clauses[random_clause_index - 1]))
                self.model[abs(random_var) - 1] = int(not self.model[abs(random_var) - 1])

            else:
                satisfied_scores = {}
                for elem in self.clauses[random_clause_index]:
                    self.model[abs(elem) - 1] = int(not self.model[abs(elem) - 1])  # temporarily flip elem's value
                    var_clauses_satisfied = 0  # how many clauses would be satisfied?
                    # go through every clause the elem's variable is in and check for clause satisfaction
                    for clause in self.var_clauses.get(abs(elem)):
                        var_clauses_satisfied += self.__is_clause_satisfied__(clause)
                    satisfied_scores[abs(elem)] = var_clauses_satisfied
                    self.model[abs(elem) - 1] = int(not self.model[abs(elem) - 1])  # undo the flipping

                # uniformly at random choose one of the vars with
                # the highest score and flip it's value
                # note that variable's index was stored
                # this can be used to access the model directly
                max_score = max(satisfied_scores.values())
                max_vars = [key for key, value in filter(lambda items: items[1] == max_score, satisfied_scores.items())]
                max_var = random.choice(max_vars)
                self.model[max_var - 1] = int(not self.model[max_var - 1])

        return 0







import random

from GSAT import GSAT

class SAT(GSAT):
    def __init__(self, cnf_file, p=0.3, max_flips=100000):
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
                max_var = None
                max_count = 0

                for var in self.clauses[random_clause_index]:
                    var_count = 0
                    for clause in self.clauses:
                        if var in clause or -var in clause:
                            var_count += self.__is_clause_satisfied__(clause)
                    if var_count > max_count:
                        max_var = var

                if max_var is not None:
                    self.model[abs(max_var) - 1] = int(not self.model[abs(max_var) - 1])
        return 0







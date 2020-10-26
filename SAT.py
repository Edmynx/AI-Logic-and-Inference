import random

from GSAT import GSAT

class SAT(GSAT):
    def __init__(self, cnf_file, p=0.3, max_flips=100000):
        GSAT.__init__(self, cnf_file, p)
        self.max_flips = max_flips
        self.satisfied = set()  # clauses that have been satisfied to date

    # check if current model satisfies all the clauses
    def __is_satisfied__(self):
        print("\n\n\ncurrent-mod", self.model)
        # for every clause yet to be satisfied
        for i in range(len(self.clauses)):
            if i not in self.satisfied:
                print("\nclauses len", len(self.clauses), self.clauses[i], "current", i)
                print("current-mod", self.model)
                for var in self.clauses[i]:
                    print("var", var)
                    # check if the variable (var) satisfies the given clause
                    # given a var i, the var index in the model is i - 1
                    if self.model[abs(var) - 1] == (0 if var < 0 else 1):
                        self.satisfied.add(i)
                        break # once the clause has been satisfied, there's no need to keep searching
                    print("satisfied", self.satisfied)

        return len(self.satisfied) == len(self.clauses)

    def walksat(self):
        for i in range(self.max_flips):
            if self.__is_satisfied__():
                print("SATISFIED.......")
                return 1

            random_clause_index = random.randint(0, len(self.clauses) - 1)
            while random_clause_index in self.satisfied:
                random_clause_index = random.randint(0, len(self.clauses) - 1)
            a = random.uniform(0, 1)
            print("prob", a)
            if a >= self.h:
                print("prob", a)
                random_var = random.choice(tuple(self.clauses[random_clause_index - 1]))
                self.model[abs(random_var) - 1] = int(not self.model[abs(random_var) - 1])

            else:
                max_var = None
                max_count = 0

                print("random clause", random_clause_index)
                print("len", len(self.clauses))
                for var in self.clauses[random_clause_index]:
                    print("len", self.clauses)
                    print("var", var)
                    var_count = 0
                    for clause in self.clauses:
                        for clause_var in clause:
                            if abs(var) == abs(clause_var):
                                if self.model[abs(var) - 1] == (0 if var < 0 else 1):
                                    print("aflfjbkkgkjgkggkkkkhkhkkhlhlllhljlljljljljljlj;jl;j;j;lj;j;;l")
                                    var_count += 1
                                    break
                    if var_count > max_count:
                        max_var = var

                print("ljljlsjfljlfdjfdjsfjds",self.model)


                self.model[abs(max_var) - 1] = int(not self.model[abs(max_var) - 1])

        return 0







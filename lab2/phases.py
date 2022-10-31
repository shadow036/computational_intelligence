from random import choice, sample
import logging
from math import ceil, floor

INVERSE_MUTATION_RATE = 20  # higher value => lower probability of mutations occurring
PARENT_SELECTION_PARAMETER = 4  # list of elements from which to choose the 2 parents

def parent_selection(e_solutions, worst_case_cost, N):
    parents =   sorted(
                    fitness_function(
                        sample(e_solutions, PARENT_SELECTION_PARAMETER), worst_case_cost, N
                    ), 
                    key=lambda t: t[1], reverse=True
                )[:2]   # list => (list, fitness)
    return [parents[_][0] for _ in range(2)]    # (list, fitness) => list

def recombination(p0, p1):
    h0 = p0[:ceil(len(p0)/2)]
    h1 = p1[floor(len(p1)/2):]
    return h0 + h1
    
def mutation(c_solutions, mu, input_):
    for index in range(mu, len(c_solutions)):
        if len(c_solutions[index]) == 1:
            m = choice(range(INVERSE_MUTATION_RATE))
            if m in [1, 2]: 
                # switch
                c_solutions[index] = input_[choice(range(len(input_)))]
            elif m in [3, 4]:    
                # add
                c_solutions[index] = [c_solutions[index], input_[choice(range(len(input_)))]]
        else:
            for index2 in range(len(c_solutions[index])):
                m = choice(range(INVERSE_MUTATION_RATE))
                if m == 0 and c_solutions[index].count(-1) != len(c_solutions[index]) - 1:  
                    # remove
                    c_solutions[index][index2] = -1
                elif m in [1, 2]: 
                    # switch
                    c_solutions[index][index2] = input_[choice(range(len(input_)))]
                elif m in [3, 4]:    
                    # add
                    c_solutions[index].append(input_[choice(range(len(input_)))])
            c_solutions[index] = [e for e in c_solutions[index] if e != -1]
    return c_solutions
        
def fitness_function(c_solutions, worst_case_cost, N):
    e_solutions = c_solutions.copy()
    # ^ in order to make clear the difference between candidate and evaluated solutions
    for index in range(len(e_solutions)):
        counters = [0 for _ in range(N)]
        for e in e_solutions[index]:
            counters = [counters[_]+1 if _ in e else counters[_] for _ in range(N)]
        partial_fitness = sum([1 - counters[_] if counters[_] > 1 
                               else counters[_] for _ in range(N)])
        offset = (worst_case_cost if counters.count(0) > 0 else 0)
        e_solutions[index] = (e_solutions[index], partial_fitness - offset)
    return e_solutions

def replacement(e_solutions, mu):
    return sorted(e_solutions, key=lambda t: t[1], reverse=True)[:mu]
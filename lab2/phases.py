from random import choice, sample
import logging
from math import ceil, floor
from hyperparameters import PARENT_SELECTION_PARAMETER, INVERSE_MUTATION_RATE, N

def parent_selection(e_solutions, total):
    parents =   sorted(
                    fitness_function(
                        sample(e_solutions, PARENT_SELECTION_PARAMETER), total
                    ), 
                    key=lambda t: t[1], reverse=True
                )[:2]   # list => (list, fitness)
    return [parents[_][0] for _ in range(2)]    # (list, fitness) => list

def recombination_plus(e_solutions, offsprings, mu, total):
    c_solutions = e_solutions.copy()
    for i in range(offsprings):
        parents = parent_selection(c_solutions[:mu], total)
        heritage0 = [parents[0]] if type(parents[0][0]) is int else parents[0][:ceil(len(parents[0])/2)]
        heritage1 = [parents[1]] if type(parents[1][0]) is int else parents[1][floor(len(parents[1])/2):]
        c_solutions.append(heritage0 + heritage1)
    return c_solutions
        
def recombination_comma(e_solutions, offsprings, total):
    c_solutions = []
    for i in range(offsprings):
        parents = parent_selection(e_solutions, total)
        heritage0 = [parents[0]] if type(parents[0][0]) is int else parents[0][:ceil(len(parents[0])/2)]
        heritage1 = [parents[1]] if type(parents[1][0]) is int else parents[1][floor(len(parents[1])/2):]
        c_solutions.append(heritage0 + heritage1)
    return c_solutions
    
def mutation(c_solutions, input_):
    for index in range(len(c_solutions)):
        m = choice(range(INVERSE_MUTATION_RATE))
        if type(c_solutions[index][0]) is int or len(c_solutions[index]) == 1:
            if m == 1: # switch
                c_solutions[index] = input_[choice(range(len(input_)))]
            elif m == 2:    # add
                c_solutions[index] = [c_solutions[index], input_[choice(range(len(input_)))]]
        else:
            for index2 in range(len(c_solutions[index])):
                if m == 0:  # remove
                    c_solutions[index][index2] = -1
                elif m == 1: # switch
                    c_solutions[index][index2] = input_[choice(range(len(input_)))]
                elif m == 2:    # add
                    c_solutions[index].append(input_[choice(range(len(input_)))])
            c_solutions[index] = [e for e in c_solutions[index] if e != -1]
    return c_solutions
        
def fitness_function(c_solutions, total):
    e_solutions = c_solutions.copy()    # in order to make clear the difference between candidate and evaluated solutions
    for index in range(len(e_solutions)):
        counters = [0 for _ in range(N)]
        if type(e_solutions[index][0]) is int:
            counters = [counters[_]+1 if _ in e_solutions[index] else counters[_] for _ in range(N)]
        else:
            for e in e_solutions[index]:
                counters = [counters[_]+1 if _ in e else counters[_] for _ in range(N)]
        partial_fitness = sum([1 - counters[_] if counters[_] > 1 else counters[_] for _ in range(N)])
        offset = (total if counters.count(0) > 0 else 0)
        e_solutions[index] = (e_solutions[index], partial_fitness - offset)
    return e_solutions

def replacement(e_solutions, mu):
    return sorted(e_solutions, key=lambda t: t[1], reverse=True)[:mu]
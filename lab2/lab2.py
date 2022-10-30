from random import choice, sample, seed, randint, shuffle
import logging
from math import inf

N = 20
INVERSE_MUTATION_RATE = 20
PARENT_SELECTION_PARAMETER = 4
GENERATIONS = 500

def problem(N, seed_=None):
    seed(seed_)
    return [
        list(set(randint(0, N - 1) for n in range(randint(N // 5, N // 2))))
        for n in range(randint(N, N * 5))
    ]

def plus_strategy(e_solutions, offsprings, mu, total):
    c_solutions = e_solutions.copy()
    for i in range(offsprings):
        parents = parent_selection(c_solutions[:mu], total)
        heritage0 = [parents[0]] if type(parents[0][0]) is int else parents[0][:randint(1, len(parents[0]))]
        heritage1 = [parents[1]] if type(parents[1][0]) is int else parents[1][randint(1, len(parents[1])):]
        c_solutions.append(heritage0 + heritage1)
    return c_solutions
        
def comma_strategy(e_solutions, offsprings, total):
    c_solutions = []
    for i in range(offsprings):
        parents = parent_selection(e_solutions, total)
        heritage0 = [parents[0]] if type(parents[0][0]) is int else parents[0][:randint(1, len(parents[0]))]
        heritage1 = [parents[1]] if type(parents[1][0]) is int else parents[1][randint(1, len(parents[1])):]
        c_solutions.append(heritage0 + heritage1)
    return c_solutions

def parent_selection(e_solutions, total):
    parents =   sorted(
                    evaluate(
                        sample(e_solutions, PARENT_SELECTION_PARAMETER), total
                    ), 
                    key=lambda t: t[1], reverse=True
                )[:2]   # list => (list, fitness)
    return [parents[_][0] for _ in range(2)]    # (list, fitness) => list

def artificial_selection(e_solutions, mu):
    return sorted(e_solutions, key=lambda t: t[1], reverse=True)[:mu]
    
def mutation(c_solutions, input_):
    for index in range(len(e_solutions)):
        m = choice(range(INVERSE_MUTATION_RATE))
        if type(c_solutions[index][0]) is int or len(c_solutions[index]) == 1:
            if m in [1, 2]: # switch
                c_solutions[index] = input_[choice(range(len(input_)))]
            elif m == 3:    # add
                c_solutions[index] = [c_solutions[index], input_[choice(range(len(input_)))]]
        else:
            for index2 in range(len(c_solutions[index])):
                if m == 0:  # remove
                    del c_solutions[index][index2]
                elif m in [1, 2]: # switch
                    c_solutions[index][index2] = input_[choice(range(len(input_)))]
                elif m == 3:    # add
                    c_solutions[index].append(input_[choice(range(len(input_)))])
    return c_solutions
        
def evaluate(c_solutions, total):
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

if __name__ == '__main__':
    global OFFSPRINGS_PLUS, OFFSPRINGS_COMMA
    input_ = problem(N, seed_=42)
    total = sum(len(l) for l in input_)
    e_solutions = input_.copy()
    current_best = [(None, -total), (None, -total)]
    mu = len(input_)
    OFFSPRINGS_PLUS = 10 * mu
    OFFSPRINGS_COMMA = mu
    for i in range(GENERATIONS):
        c_solutions = plus_strategy(e_solutions, OFFSPRINGS_PLUS, mu, total) # list => list
        c_solutions = mutation(e_solutions, input_) # list => list
        e_solutions = evaluate(c_solutions, total) # list => (list, fitness)
        e_solutions = artificial_selection(e_solutions, mu)    # (list, fitness) => (list, fitness)
        if current_best[0][1] < e_solutions[0][1]:
            current_best[0] = (e_solutions[0][0], e_solutions[0][1])
        print(current_best[0][1])
        e_solutions = [e_solutions[_][0] for _ in range(len(e_solutions))]  # (list, fitness) => list
    e_solutions = input_.copy()
    for i in range(GENERATIONS):
        c_solutions = comma_strategy(e_solutions, OFFSPRINGS_COMMA, total) # list => list
        c_solutions = mutation(e_solutions, input_) # list => list
        e_solutions = evaluate(c_solutions, total) # list => (list, fitness)
        e_solutions = artificial_selection(e_solutions, mu)    # (list, fitness) => (list, fitness)
        if current_best[1][1] < e_solutions[0][1]:
            current_best[1] = (e_solutions[0][0], e_solutions[0][1])
        print(current_best[1][1])
        e_solutions = [e_solutions[_][0] for _ in range(len(e_solutions))]  # (list, fitness) => list

from phases import parent_selection, recombination, mutation, fitness_function, replacement
from utilities import problem, hide_fitness

N = 50
GENERATIONS = 10    # other than the initial one

if __name__ == '__main__':
    input_ = problem(N, seed_=42)
    worst_case_cost = sum(len(l) for l in input_) - N
    current_best = [None, None]
    mu = len(input_)
    offsprings = [mu, 10 * mu]  # lambdas for plus and comma strategy

    # PLUS STRATEGY
    c_solutions = [[i] for i in input_]
    e_solutions = fitness_function(c_solutions, worst_case_cost, N)
    current_best[0] = sorted(e_solutions, key=lambda t: t[1], reverse=True)[0]
    for i in range(GENERATIONS):
        c_solutions = hide_fitness(e_solutions)
        for j in range(offsprings[0]):
            p0, p1 = parent_selection(c_solutions[:mu], worst_case_cost, N)
            c_solutions.append(recombination(p0, p1))
        c_solutions = mutation(c_solutions, mu, input_)
        e_solutions = fitness_function(c_solutions, worst_case_cost, N)
        e_solutions = replacement(e_solutions, mu)
        if e_solutions[0][1] > current_best[0][1]:
            current_best[0] = e_solutions[0]
    
    # COMMA STRATEGY
    c_solutions = [[i] for i in input_]
    e_solutions = fitness_function(c_solutions, worst_case_cost, N)
    current_best[1] = sorted(e_solutions, key=lambda t: t[1], reverse=True)[0]
    for i in range(GENERATIONS):
        possible_parents = hide_fitness(e_solutions)
        c_solutions = []
        for j in range(offsprings[1]):
            p0, p1 = parent_selection(possible_parents, worst_case_cost, N)
            c_solutions.append(recombination(p0, p1))
        c_solutions = mutation(c_solutions, 0, input_)
        e_solutions = fitness_function(c_solutions, worst_case_cost, N)
        e_solutions = replacement(e_solutions, mu)
        if e_solutions[0][1] > current_best[1][1]:
            current_best[1] = e_solutions[0]
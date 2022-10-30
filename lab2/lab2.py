from phases import parent_selection, recombination_plus, recombination_comma, mutation, fitness_function, replacement
from hyperparameters import N, GENERATIONS
from utilities import problem, hide_fitness

if __name__ == '__main__':
    input_ = problem(N, seed_=42)
    total = sum(len(l) for l in input_)
    e_solutions = input_.copy()
    current_best = [(None, -total), (None, -total)]
    mu = len(input_)
    offsprings_plus = 10 * mu
    offsprings_comma = mu
    for i in range(GENERATIONS):
        c_solutions = recombination_plus(e_solutions, offsprings_plus, mu, total) # list => list
        c_solutions = mutation(e_solutions, input_) # list => list
        e_solutions = fitness_function(c_solutions, total) # list => (list, fitness)
        e_solutions = replacement(e_solutions, mu)    # (list, fitness) => (list, fitness)
        if current_best[0][1] < e_solutions[0][1]:
            current_best[0] = (e_solutions[0][0], e_solutions[0][1])
        print(current_best[0][1])
        e_solutions = hide_fitness(e_solutions)  # (list, fitness) => list
    # e_solutions = input_.copy()
    # for i in range(GENERATIONS):
    #     c_solutions = recombination_comma(e_solutions, OFFSPRINGS_COMMA, total) # list => list
    #     #c_solutions = mutation(e_solutions, input_) # list => list
    #     e_solutions = fitness_function(c_solutions, total) # list => (list, fitness)
    #     e_solutions = artificial_selection(e_solutions, mu)    # (list, fitness) => (list, fitness)
    #     if current_best[1][1] < e_solutions[0][1]:
    #         current_best[1] = (e_solutions[0][0], e_solutions[0][1])
    #     print(current_best[1][1])
    #     e_solutions = [e_solutions[_][0] for _ in range(len(e_solutions))]  # (list, fitness) => list

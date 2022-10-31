from phases import parent_selection, recombination, mutation, fitness_function, replacement
from utilities import problem, hide_fitness
from logging import info, debug, basicConfig, DEBUG

Ns = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 500, 1000]
GENERATIONS = 1000    # other than the initial one

if __name__ == '__main__':
    results = []
    for N in Ns:
        debug(f'N = {N}')
        input_ = problem(N, seed_=42)
        worst_case_fitness = sum(len(l) for l in input_) - N
        current_best = [None, None]
        mu = len(input_)
        offsprings = [mu, 10 * mu]  # lambdas for plus and comma strategy
        basicConfig(level=DEBUG)
    
        # PLUS STRATEGY
        c_solutions = [[i] for i in input_]
        e_solutions = fitness_function(c_solutions, worst_case_fitness, N)
        current_best[0] = sorted(e_solutions, key=lambda t: t[1], reverse=True)[0]
        for gen in range(GENERATIONS):
            c_solutions = hide_fitness(e_solutions)
            for o in range(offsprings[0]):
                p0, p1 = parent_selection(c_solutions[:mu], worst_case_fitness, N)
                c_solutions.append(recombination(p0, p1))
            c_solutions = mutation(c_solutions, mu, current_best[0][1] < 0, input_)
            e_solutions = fitness_function(c_solutions, worst_case_fitness, N)
            e_solutions = replacement(e_solutions, mu)
            if e_solutions[0][1] > current_best[0][1]:
                current_best[0] = e_solutions[0]
                debug(f'new solution (strategy: "plus", fitness: {current_best[0][1]}, generation: {gen})')
            if current_best[0][1] == N: # optimal solution found!
                debug('optimal solution found!')
                break
        if N < 50:
            # COMMA STRATEGY
            c_solutions = [[i] for i in input_]
            e_solutions = fitness_function(c_solutions, worst_case_fitness, N)
            current_best[1] = sorted(e_solutions, key=lambda t: t[1], reverse=True)[0]
            for gen in range(GENERATIONS):
                possible_parents = hide_fitness(e_solutions)
                c_solutions = []
                for o in range(offsprings[1]):
                    p0, p1 = parent_selection(possible_parents, worst_case_fitness, N)
                    c_solutions.append(recombination(p0, p1))
                c_solutions = mutation(c_solutions, mu, current_best[1][1] < 0, input_)
                e_solutions = fitness_function(c_solutions, worst_case_fitness, N)
                e_solutions = replacement(e_solutions, mu)
                if e_solutions[0][1] > current_best[1][1]:
                    current_best[1] = e_solutions[0]
                    debug(f'new solution (strategy: "comma", fitness: {current_best[1][1]}, generation: {gen})')
                if current_best[1][1] == N: # optimal solution found!
                    debug('optimal solution found!')
                    break
        results.append(current_best)
    
    for i, N in enumerate(Ns):
        info(f'N: {N} => (fitness "plus" strategy: {results[i][0][1]}, fitness "comma" strategy: {results[i][1][1]})')
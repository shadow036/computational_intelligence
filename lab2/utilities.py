from random import randint, seed

def problem(N, seed_=None):
    seed(seed_)
    return [
        list(set(randint(0, N - 1) for n in range(randint(N // 5, N // 2))))
        for n in range(randint(N, N * 5))
    ]

def hide_fitness(e_solutions):
    return [e_solutions[_][0] for _ in range(len(e_solutions))]
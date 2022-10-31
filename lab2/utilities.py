from random import randint, seed, choice

def problem(N, seed_=None):
    seed(seed_)
    return [
        list(set(randint(0, N - 1) for n in range(randint(N // 5, N // 2))))
        for n in range(randint(N, N * 5))
    ]

def hide_fitness(e_solutions):
    return [e_solutions[_][0] for _ in range(len(e_solutions))]

def exploration_vs_exploitation(m, flag, c_solutions, index, index2, input_):
    if flag is True:    # exploration
        if m == 0 and c_solutions[index].count(-1) != len(c_solutions[index]) - 1:  
            # remove - 10% chance
            c_solutions[index][index2] = -1
        elif m in [1, 2]: 
            # switch - 20% chance
            c_solutions[index][index2] = input_[choice(range(len(input_)))]
        elif m in [3, 4, 5]:    
            # add - 30% chance
            c_solutions[index].append(input_[choice(range(len(input_)))])
    else:   # exploitation
        if m == 0 and c_solutions[index].count(-1) != len(c_solutions[index]) - 1:  
            # remove - 10% chance
            c_solutions[index][index2] = -1
        elif m in [1, 2, 3]: 
            # switch - 30% chance
            c_solutions[index][index2] = input_[choice(range(len(input_)))]
        elif m == 5:    
            # add - 10% chance
            c_solutions[index].append(input_[choice(range(len(input_)))])
    return c_solutions[index]
import random
import logging
import numpy as np

FOUND = 2
CONTINUE = 1
ROLLBACK = 0

DEBUG = 1
DEBUG2 = 0

def problem(N, seed=None):
    """generates a list of sublists containing a variable number of integers from 0 to N-1"""
    random.seed(seed)
    return [
        list(set(random.randint(0, N - 1) for n in range(random.randint(N // 5, N // 2))))
        for n in range(random.randint(N, N * 5))
    ]

class State:
    """
    chosen_sublists: list of indices of chosen sublists
    numbers_occurrences: array of counters (example -> numbers_occurrences[0]: how many times the number 0 appears in all chosen sublists)
    amount_visited_nodes: number of visited nodes until now
    """
    def __init__(self, chosen_sublists, numbers_occurrences, amount_visited_nodes):
        self.chosen_sublists = chosen_sublists
        self.numbers_occurrences = numbers_occurrences
        self.cost = sum(numbers_occurrences)
        self.amount_visited_nodes = amount_visited_nodes

class Solution:
    """n: external parameter"""
    """cost: cost of currently best solution"""
    """solution: list of indices of sublists included in the currently best solution"""
    """amount_visited_nodes: amount of visited nodes needed to reach currently best solution"""
    def __init__(self, n, cost, solution, amount_visited_nodes):
        self.n = n
        self.cost = cost
        self.bloat = 100 * (cost - n)/n
        self.solution = solution
        self.amount_visited_nodes = amount_visited_nodes

def search(n, state, current_solution, index, list_, visited_nodes, depth):
    """recursive search for solution"""
    numbers_occurrences = state.numbers_occurrences.copy()
    if index > -1:
        for i in list_[index]:
            numbers_occurrences[i] += 1
        new_state = State([index] if len(state.chosen_sublists) == 0 else state.chosen_sublists + [index], numbers_occurrences, visited_nodes)
        command1 = check_state(n, new_state, current_solution, list_, depth)
    else:
        new_state = state
    if index == -1 or command1 == CONTINUE:
        if index > -1:
            current_solution, command2 = check_goal(new_state, current_solution, n)
            visited_nodes += 1
            new_state.amount_visited_nodes = visited_nodes
        if index == -1 or command2 == CONTINUE:
            for i in range(index + 1, len(list_)):
                current_solution, visited_nodes = search(n, new_state, current_solution, i, list_, visited_nodes, depth + 1)
    return current_solution, visited_nodes

def check_goal(state, current_solution, n):
    """check if a new solution (better than the previous one) has been found"""
    if all(state.numbers_occurrences) and state.cost < current_solution.cost:
        if DEBUG:
            logging.info(f'(n: {n}, solution: {state.chosen_sublists}, bloat: {100 * (state.cost - n)/n}%)')
        return Solution(n, state.cost, state.chosen_sublists, state.amount_visited_nodes), FOUND
    else:
        return current_solution, CONTINUE

def check_state(n, state, current_solution, list_, depth):
    bloat = 100 * (state.cost - n)/n
    """checks if new state is useful"""
    # incomplete solution + cost already higher than the optimal one
    if all(state.numbers_occurrences) == False and sum(state.numbers_occurrences) >= current_solution.cost:
        if DEBUG2:
            logging.info(f'(n: {n}, rollback #1: {state.chosen_sublists}')
        return ROLLBACK
    # last sublist added was useless (cost increase without getting closer to the solution)
    elif all(state.numbers_occurrences[v] > 1 for v in list_[state.chosen_sublists[-1]]):
        if DEBUG2:
            logging.info(f'(n: {n}, rollback #2: {state.chosen_sublists}')
        return ROLLBACK
    # bound regarding depth and bloat in order to speed up computations - applied only in case of large Ns
    elif (depth > 8 or bloat > 100) and n > 20:
        if DEBUG2:
            logging.info(f'(n: {n}, rollback #3: {state.chosen_sublists}')
        return ROLLBACK
    else:
        return CONTINUE

def custom_dfs(n):
    """wrapper for custom depth-first search algorithm"""
    list_ = problem(n, seed=42)
    solution = Solution(n, sum(len(i) for i in list_), None, 0)
    initial_state = State([], np.zeros(n), 0)
    solution, _ = search(n, initial_state, solution, -1, list_, 0, 0)
    return solution
    
if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    solutions = []
    for n in [5, 10, 20, 100, 500, 1000]:
        solutions.append(custom_dfs(n))
    for s in solutions:
        print(f'\nn: {s.n}\ncost: {s.cost} -> bloat: {s.bloat}%\nsolution: {s.solution}\nvisited nodes: {s.amount_visited_nodes}')



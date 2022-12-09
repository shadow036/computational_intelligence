from strategies.utilities import Nim
from strategies.utilities import evaluate, get_all_strategies, run_tournament
from strategies.utilities import N_ROWS, N_MATCHES, STRATEGIES

from strategies.evolving_agents import make_substrategy, substrategies_mutation

from strategies.reinforcement import Agent
from strategies.reinforcement import get_possible_actions

from random import randint, random

if __name__ == '__main__':
    # FIXED RULES ------------------------------------------------------------------------------------------------------
    """strategies = get_all_strategies()
    global_win_rates = run_tournament(strategies, N_ROWS, N_MATCHES)
    evaluate(strategies, N_ROWS, N_MATCHES, indices=(randint(0, len(strategies) - 1), randint(0, len(strategies) - 1)))
    """
    # EVOLVED RULES ----------------------------------------------------------------------------------------------------
    """indices = [randint(17, 23) for _ in range(50)]
    initial_pool = [make_substrategy(strategies[index], index, random()) for index in indices]
    run_tournament(initial_pool, N_ROWS, N_MATCHES)
    new_pool = []
    new_s = None
    for st in initial_pool:
        if random() > 0.5:
            target = randint(0, len(strategies) - 1)
            new_s = substrategies_mutation(STRATEGIES[target], 0, strategies[target])
        new_pool.append(new_s)"""
    # REINFORCEMENT ----------------------------------------------------------------------------------------------------
    environment = Nim(N_ROWS)
    agent = Agent(environment.get_nrows)
    while environment:
        possible_action = get_possible_actions(environment.get_rows, environment.get_nrows)
        if random() <= agent.get_learning_rate():
            best_action = possible_action[randint(0, len(possible_action) - 1)]
        else:
            best_action = agent.choose_best_action(possible_action)
        environment.nimming((best_action[0], best_action[1] + 1))
        agent.learn()

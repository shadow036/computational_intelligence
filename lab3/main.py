from game_utilities import run_tournament, evaluate,   # useful functions
from game_utilities import N_ROWS, MATCHES  # constants
from game_utilities import DIVERGENT, DIVERGENT_CHALLENGER, SPREADER, AGGRESSIVE_SPREADER, NIMSUM_LITTLE_BROTHER, \
    OPTIMAL_STRATEGY, PURE_RANDOM, GABRIELE, MAKE_STRATEGY_1, MAKE_STRATEGY_5, MAKE_STRATEGY_9, DUMMY, \
    DIVERGENT_TRIPHASE, THE_BALANCER, THE_MIRRORER, THE_REVERSED_MIRRORER, S_DIVERGENT, S_THE_MIRRORER, \
    S_THE_REVERSED_MIRRORER, S_THE_BALANCER, S_NIMSUM_LITTLE_BROTHER, S_GABRIELE, S_SPREADER, S_PURE_RANDOM, CUSTOM
from strategies.strategy_utilities import make_strategy, make_substrategy, substrategies_mutation  # strategy generator
from strategies.fixed_rules import optimal_strategy, dummy, pure_random, gabriele, spreader, aggressive_spreader, \
    nimsum_little_brother, divergent, divergent_challenger, divergent_triphase, the_balancer, the_mirrorer, random_spreader, \
    the_reversed_mirrorer   # fixed rules strategies
from strategies.evolving_agents import s_divergent, s_the_balancer, s_the_reversed_mirrorer, \
    s_gabriele, s_spreader, s_pure_random, s_nimsum_little_brother  # substrategies used for evolving
from random import randint, random


if __name__ == '__main__':
    strategies = [
        divergent, divergent_challenger, spreader, aggressive_spreader, nimsum_little_brother, optimal_strategy,
        pure_random, gabriele, make_strategy(0.1), make_strategy(0.5), make_strategy(0.9), dummy, divergent_triphase,
        the_balancer, the_mirrorer, random_spreader, the_reversed_mirrorer,

        s_divergent, s_the_balancer, s_the_reversed_mirrorer, s_gabriele, s_spreader, s_pure_random,
        s_nimsum_little_brother
    ]
    #
    # global_win_rates = run_tournament(strategies, N_ROWS, MATCHES)  # tournament fixed agents
    # evaluate(strategies, N_ROWS, MATCHES, indices=(THE_REVERSED_MIRRORER, SPREADER))   # used to directly compare
    # two agents

    indices = [randint(17, 23) for _ in range(50)]
    initial_pool = [make_substrategy(strategies[index], index, random()) for index in indices]
    run_tournament(initial_pool, N_ROWS, MATCHES)
    new_pool = []
    for st in initial_pool:
        if random() > 0.5:
            new_s = substrategies_mutation()
        new_pool.append(new_s)

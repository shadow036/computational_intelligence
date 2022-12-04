from game_utilities import run_tournament, evaluate  # useful functions
from game_utilities import N_ROWS, MATCHES  # constants
from game_utilities import DIVERGENT, DIVERGENT_CHALLENGER, SPREADER, AGGRESSIVE_SPREADER, NIMSUM_LITTLE_BROTHER, \
    OPTIMAL_STRATEGY, PURE_RANDOM, GABRIELE, MAKE_STRATEGY_1, MAKE_STRATEGY_5, MAKE_STRATEGY_9, DUMMY, DIVERGENT_TRIPHASE, \
    THE_BALANCER, THE_MIRRORER, THE_REVERSED_MIRRORER
from strategies.strategy_utilities import make_strategy  # strategy generator
from strategies.fixed_rules import optimal_strategy, dummy, pure_random, gabriele, spreader, aggressive_spreader, \
    nimsum_little_brother, divergent, divergent_challenger, divergent_triphase, the_balancer, the_mirrorer, random_spreader, \
    the_reversed_mirrorer   # fixed rules strategies

if __name__ == '__main__':
    strategies = [
        divergent, divergent_challenger, spreader, aggressive_spreader, nimsum_little_brother, optimal_strategy,
        pure_random, gabriele, make_strategy(0.1), make_strategy(0.5), make_strategy(0.9), dummy, divergent_triphase,
        the_balancer, the_mirrorer, random_spreader, the_reversed_mirrorer
    ]

    global_win_rates = run_tournament(strategies, N_ROWS, MATCHES)  # tournament

    #evaluate(strategies, N_ROWS, MATCHES, indices=(THE_REVERSED_MIRRORER, SPREADER))

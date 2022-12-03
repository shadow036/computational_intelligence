from game_utilities import run_tournament, evaluate  # useful functions
from game_utilities import N_ROWS, MATCHES  # constants
from strategies.strategy_utilities import HEL, HEL_CHALLENGER, SPREADER, AGGRESSIVE_SPREADER, NIMSUM_LIL_BROTHER, \
    OPTIMAL_STRATEGY, PURE_RANDOM, GABRIELE, MAKE_STRATEGY_1, MAKE_STRATEGY_5, MAKE_STRATEGY_9, DUMMY, HEL_TRIPHASE, \
    SEMI_SELF_ADAPTER
from strategies.strategy_utilities import make_strategy  # strategy generator
from strategies.fixed_rules import optimal_strategy, dummy, pure_random, gabriele, spreader, aggressive_spreader, \
    nimsum_lil_brother, hel, hel_challenger, hel_triphase, semi_self_adapter   # fixed rules strategies

if __name__ == '__main__':
    strategies = [
        hel, hel_challenger, spreader, aggressive_spreader, nimsum_lil_brother, optimal_strategy,
        pure_random, gabriele, make_strategy(0.1), make_strategy(0.5), make_strategy(0.9), dummy, hel_triphase
                  ]

    # global_win_rates = run_tournament(strategies, N_ROWS, MATCHES)  # tournament

    evaluate(aggressive_spreader, hel_challenger, N_ROWS, MATCHES, indices=(AGGRESSIVE_SPREADER, HEL_CHALLENGER))

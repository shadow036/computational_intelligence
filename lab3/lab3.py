from utilities import N_ROWS, N_MATCHES, LEARNING_TURNS, STRATEGIES
from utilities import Nim
from utilities import evaluate, run_tournament

from strategies.fixed_rules import optimal_strategy, divergent, divergent_challenger, spreader, aggressive_spreader, \
    nimsum_little_brother, pure_random, gabriele, make_strategy, dummy, divergent_triphase, the_balancer, \
    the_mirrorer, random_spreader, the_reversed_mirrorer
from strategies.fixed_rules import PURE_RANDOM, NIMSUM_LITTLE_BROTHER, OPTIMAL_STRATEGY, \
    SPREADER, THE_REVERSED_MIRRORER, THE_MIRRORER, GABRIELE, MAKE_STRATEGY_1, MAKE_STRATEGY_5, MAKE_STRATEGY_9, DUMMY, \
    DIVERGENT, DIVERGENT_CHALLENGER, DIVERGENT_TRIPHASE, AGGRESSIVE_SPREADER, THE_BALANCER, RANDOM_SPREADER

from strategies.evolving_agents import s_divergent, s_the_balancer, s_the_reversed_mirrorer, \
    s_gabriele, s_spreader, s_pure_random, s_nimsum_little_brother

from strategies.min_max import MinMax
from strategies.min_max import MY_TURN, OPPONENT_TURN, MINMAX

from strategies.reinforcement import Agent, REINFORCEMENT
from strategies.reinforcement import get_possible_actions, evaluate_state, make_hashable, show_learning_progress, \
    choose_best_action

from random import randint, random
import numpy as np

if __name__ == '__main__':
    agent = Agent(N_ROWS)
    minmax = MinMax(N_ROWS, MY_TURN)
    minmax.add_actions_nodesRewards()

    strategies = [divergent, divergent_challenger, spreader, aggressive_spreader, nimsum_little_brother,
                  optimal_strategy, pure_random, gabriele, make_strategy(0.1), make_strategy(0.5), make_strategy(0.9),
                  dummy, divergent_triphase, the_balancer, the_mirrorer, random_spreader, the_reversed_mirrorer,

                  s_divergent, s_the_balancer, s_the_reversed_mirrorer, s_gabriele, s_spreader,
                  s_pure_random,
                  s_nimsum_little_brother,

                  agent.play,
                  minmax.play
                  ]
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
    # MIN MAX ----------------------------------------------------------------------------------------------------------
    minmax.visualize_tree()
    evaluate(strategies, N_ROWS, N_MATCHES, indices=(MINMAX, SPREADER), minmax_reset=minmax)
    # REINFORCEMENT ----------------------------------------------------------------------------------------------------
    """history = []
    opponent = PURE_RANDOM
    print(f'Learning progress vs {STRATEGIES[opponent]}')
    old = -1
    for turn in range(LEARNING_TURNS):
        new = int(100 * turn/LEARNING_TURNS)
        if new > old:
            print(show_learning_progress(new))
            old = new
        environment = Nim(N_ROWS)
        if opponent in [THE_MIRRORER, THE_REVERSED_MIRRORER]:
            mirror_flags = (environment.get_nrows, sum(environment.get_rows))
            reverse_mirror_flags = (environment.get_nrows, environment.get_rows)
        agent.reset_state_list()
        agent.decrease_exploration_rate(1.9e-6 if turn > 0 else 0)
        history.append(agent.get_beliefs())
        while environment:
            possible_actions = get_possible_actions(environment.get_rows, environment.get_nrows)
            if random() <= agent.get_exploration_rate():
                target = np.random.choice(len(possible_actions))
                best_action = possible_actions[target]
            else:
                best_action = choose_best_action(possible_actions, environment, agent)
            environment.nimming((best_action[0], best_action[1] + 1))
            agent.add_state_list(make_hashable(environment.get_rows), evaluate_state(environment.get_rows))
            if environment:
                if opponent == THE_MIRRORER:
                    ply, mirror_flags = the_mirrorer(environment, mirror_flags)
                elif opponent == THE_REVERSED_MIRRORER:
                    ply, reverse_mirror_flags = the_reversed_mirrorer(environment, reverse_mirror_flags)
                else:
                    ply = strategies[opponent](environment)
                environment.nimming(ply)
        agent.learn()
        minmax.reset_minmax()
    evaluate(strategies, N_ROWS, N_MATCHES, indices=(REINFORCEMENT, opponent), minmax_reset=minmax)"""

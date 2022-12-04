import logging
from typing import Callable
import random
from copy import deepcopy
import numpy as np
from itertools import accumulate
from operator import xor


# player IDs
PLAYER1 = 0
PLAYER2 = 1
# statistics indices for the 'evaluate function'
STARTING_FIRST = 1
STARTING_SECOND = 0
WINS = 0
TOTAL = 1
# strategy names
STRATEGIES = ['hel', 'hel_challenger', 'spreader', 'aggressive_spreader', 'nimsum_lil_brother', 'optimal_strategy',
              'pure_random', 'gabriele', 'make_strategy(0.1)', 'make_strategy(0.5)', 'make_strategy(0.9)', 'dummy',
              'hel_triphase', 'the_balancer', 'the_mirrorer']

# strategies which were already present
OPTIMAL_STRATEGY = 5
PURE_RANDOM = 6
GABRIELE = 7
MAKE_STRATEGY_1 = 8
MAKE_STRATEGY_5 = 9
MAKE_STRATEGY_9 = 10
DUMMY = 11
# my strategies
HEL = 0
HEL_CHALLENGER = 1
SPREADER = 2
AGGRESSIVE_SPREADER = 3
NIMSUM_LIL_BROTHER = 4
HEL_TRIPHASE = 12
THE_BALANCER = 13
THE_MIRRORER = 14
# hyperparameters for the 'evaluate' and 'tournament' functions
N_ROWS = 11
MATCHES = 10
K = None


class Nim:
    def __init__(self, num_rows: int, k=None) -> None:
        self.rows = [i * 2 + 1 for i in range(num_rows)]
        self.original_rows = self.rows.copy()
        self.k = k
        self.mirror_flags = num_rows, sum(self.rows)

    def __bool__(self):
        return sum(self.rows) > 0

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self.rows) + ">"

    @property
    def return_rows(self) -> tuple:
        return tuple(self.rows)

    @property
    def return_original_rows(self) -> tuple:
        return tuple(self.original_rows)

    @property
    def return_mirror_flags(self):
        return self.mirror_flags

    def set_mirror_flags(self, n_flags):
        self.mirror_flags = n_flags

    @property
    def return_nrows(self) -> int:
        return len(self.rows)

    @property
    def return_k(self) -> int:
        return self.k

    def nimming(self, ply: tuple) -> None:
        row, num_objects = ply
        assert self.rows[row] >= num_objects
        assert self.k is None or num_objects <= self.k
        self.rows[row] -= num_objects


def evaluate(strategy: Callable, benchmark: Callable, n_rows, matches, indices, tournament=False):
    logging.getLogger().setLevel(logging.DEBUG)
    strategies = (strategy, benchmark)
    my_win_rates = np.zeros((2, 2))
    starting_player = random.choice([PLAYER1, PLAYER2])
    for _ in range(matches):
        nim = Nim(num_rows=n_rows)
        player = starting_player
        if not tournament:
            logging.debug(f"status: Initial board  -> {nim}")
        while nim:
            ply = strategies[player](nim)
            nim.nimming(ply)
            if not tournament:
                logging. \
                    debug(f"status: After {STRATEGIES[indices[player]]} turn -> {nim}")
            player = 1 - player
        winner = 1 - player
        if not tournament:
            logging. \
                info(f"status: {STRATEGIES[indices[winner]]} won!")
        my_win_rates[WINS, int(starting_player == PLAYER1)] += int(winner == PLAYER1)
        my_win_rates[TOTAL, int(starting_player == PLAYER1)] += 1
        starting_player = 1 - starting_player
    my_win_rate = round(100 * sum(my_win_rates[WINS, :])/matches)
    opponent_win_rate = 100 - my_win_rate
    if not tournament:
        my_win_rate_starting_first = round(100 *
                                           my_win_rates[WINS, STARTING_FIRST]/my_win_rates[TOTAL, STARTING_FIRST])
        my_win_rate_starting_second = round(100 *
                                            my_win_rates[WINS, STARTING_SECOND]/my_win_rates[TOTAL, STARTING_SECOND])
        opponent_win_rate_starting_first = 100 - my_win_rate_starting_second
        opponent_win_rate_starting_second = 100 - my_win_rate_starting_first
        win_rate_starting_first = 100 * (my_win_rates[WINS, STARTING_FIRST] + my_win_rates[TOTAL, STARTING_SECOND] -
                                         my_win_rates[WINS, STARTING_SECOND])/matches
        win_rate_starting_second = 100 * (my_win_rates[WINS, STARTING_SECOND] + my_win_rates[TOTAL, STARTING_FIRST] -
                                          my_win_rates[WINS, STARTING_FIRST])/matches
        print(f'\n{STRATEGIES[indices[PLAYER1]]} win rate: {my_win_rate}%')
        print(f'{STRATEGIES[indices[PLAYER1]]} win rate starting first: {my_win_rate_starting_first}%')
        print(f'{STRATEGIES[indices[PLAYER1]]} win rate starting second: {my_win_rate_starting_second}%')
        print(f'\n{STRATEGIES[indices[PLAYER2]]} win rate: {opponent_win_rate}%')
        print(f'{STRATEGIES[indices[PLAYER2]]} win rate starting first: {opponent_win_rate_starting_first}%')
        print(f'{STRATEGIES[indices[PLAYER2]]} win rate starting second: {opponent_win_rate_starting_second}%')
        print(f'\nprobability of winning when starting first: {win_rate_starting_first}%')
        print(f'probability of winning when starting second: {win_rate_starting_second}%\n')
        return [my_win_rates, my_win_rate_starting_first, my_win_rate_starting_second], \
            [opponent_win_rate, opponent_win_rate_starting_first, opponent_win_rate_starting_second], \
            [win_rate_starting_first, win_rate_starting_second]
    return my_win_rate > 50, opponent_win_rate > 50


def get_info(state: Nim) -> dict:
    info = dict()
    # returns a list of (rows index, amount of objects to remove)
    info["possible_moves"] = [
        (r, o) for r, c in enumerate(state.return_rows) for o in range(1, c + 1)
        if state.return_k is None or o <= state.return_k
    ]
    info["shortest_row"] = min((x for x in enumerate(state.return_rows)
                                if x[1] > 0), key=lambda y: y[1])[0]
    info["longest_row"] = max((x for x in enumerate(state.return_rows)),
                              key=lambda y: y[1])[0]
    info["nim_sum"] = nim_sum(state)
    info["remaining rows"] = sum([int(x > 0) for x in state.return_rows])
    info["rows with more than 1"] = sum([int(x > 1) for x in state.return_rows])
    info["rows with 1"] = sum([int(x == 1) for x in state.return_rows])
    info["rows with 0"] = sum([int(x == 0) for x in state.return_rows])
    brute_force = []
    p_moves = info["possible_moves"]
    for m in p_moves:
        tmp = deepcopy(state)
        tmp.nimming(m)
        brute_force.append((m, nim_sum(tmp)))
    info["brute_force"] = brute_force
    return info


def run_tournament(strategies, k, matches):
    global_win_rates = np.zeros(len(strategies))
    for i in range(len(strategies) - 1):
        for j in range(i+1, len(strategies)):
            w1, w2 = evaluate(strategies[i], strategies[j], k, matches, (i, j), tournament=True)
            global_win_rates[i] += w1
            global_win_rates[j] += w2
        print(f'{STRATEGIES[i]}: {round(100 * global_win_rates[i]/(len(strategies) - 1), 3)}%')
    print(f'{STRATEGIES[-1]}: {round(100 * global_win_rates[-1] / (len(strategies) - 1), 3)}%')
    global_win_rates = 100 * global_win_rates / (len(strategies) - 1)
    return global_win_rates


def nim_sum(state: Nim) -> int:
    *_, result = accumulate(state.return_rows, xor)
    return result

import logging
import random
from copy import deepcopy
import numpy as np
from itertools import accumulate
from operator import xor
from strategies.min_max import MINMAX, MinMax

N_ROWS = 6
N_MATCHES = 10000
LEARNING_TURNS = 100000
K = None

PLAYER1 = 0
PLAYER2 = 1

STARTING_FIRST = 1
STARTING_SECOND = 0

WINS = 0
TOTAL = 1

CUSTOM = -1
THE_MIRRORER = 14
THE_REVERSED_MIRRORER = 16
S_THE_REVERSED_MIRRORER = 19

STRATEGIES = ['divergent', 'divergent_challenger', 'spreader', 'aggressive_spreader', 'nimsum_little_brother',
              'optimal_strategy',
              'pure_random', 'gabriele', 'make_strategy(0.1)', 'make_strategy(0.5)', 'make_strategy(0.9)', 'dummy',
              'divergent_triphase', 'the_balancer', 'the_mirrorer', 'random_spreader', 'the_reversed_mirrorer',

              's_divergent', 's_the_balancer', 's_the_reversed_mirrorer', 's_gabriele', 's_spreader',
              's_pure_random',
              's_nimsum_little_brother',
              'reinforced',
              'min_max',

              'custom'
              ]


class Nim:
    def __init__(self, num_rows: int, k=None) -> None:
        self.rows = [i * 2 + 1 for i in range(num_rows)]
        self.original_rows = self.rows.copy()
        self.k = k

    def __bool__(self):
        return bool(sum(self.rows) > 0)

    def __str__(self):
        return "<" + " ".join(str(_) for _ in self.rows) + ">"

    @property
    def get_rows(self) -> tuple:
        return tuple(self.rows)

    @property
    def get_original_rows(self) -> tuple:
        return tuple(self.original_rows)

    @property
    def get_nrows(self) -> int:
        return len(self.rows)

    @property
    def get_k(self) -> int:
        return self.k

    def set_rows(self, rows):
        self.rows = rows

    def nimming(self, ply: tuple) -> None:
        row, num_objects = ply
        assert self.rows[row] >= num_objects
        assert self.k is None or num_objects <= self.k
        self.rows[row] -= num_objects


def evaluate(strategies: list, n_rows, matches, indices=None, tournament=False, players=None, minmax_reset=None):
    logging.getLogger().setLevel(logging.DEBUG)
    if players is None:
        strategies = (strategies[indices[PLAYER1]], strategies[indices[PLAYER2]])
    else:
        strategies = (players[0], players[1])
    my_win_rates = np.zeros((2, 2))
    starting_player = random.choice([PLAYER1, PLAYER2])
    for _ in range(matches):
        nim = Nim(num_rows=n_rows)
        mirror_flags = [(nim.get_nrows, sum(nim.get_rows)), (nim.get_nrows, sum(nim.get_rows))]
        reverse_mirror_flags = \
            [(nim.get_nrows, nim.get_rows), (nim.get_nrows, nim.get_rows)]
        player = starting_player
        if not tournament:
            logging.debug(f"status: Initial board  -> {nim}")
        while nim:
            if indices[player] == THE_MIRRORER:
                ply, mirror_flags[player] = strategies[player](nim, mirror_flags[player])
            elif indices[player] == THE_REVERSED_MIRRORER or indices[player] == S_THE_REVERSED_MIRRORER:
                ply, reverse_mirror_flags[player] = strategies[player](nim, reverse_mirror_flags[player])
            else:
                ply = strategies[player](nim)
            nim.nimming(ply)
            if not tournament:
                logging. \
                    debug(f"status: After {STRATEGIES[indices[player]]}"
                          f"{'#' + str(player) if indices[player] == CUSTOM else ''} turn -> {nim}")
            player = 1 - player
        winner = 1 - player
        if not tournament:
            logging. \
                info(f"status: {STRATEGIES[indices[winner]]} won!")
        if MINMAX in indices:
            minmax_reset.reset_minmax()
        my_win_rates[WINS, int(starting_player == PLAYER1)] += int(winner == PLAYER1)
        my_win_rates[TOTAL, int(starting_player == PLAYER1)] += 1
        starting_player = 1 - starting_player
    my_win_rate = round(100 * sum(my_win_rates[WINS, :]) / matches)
    opponent_win_rate = 100 - my_win_rate
    if not tournament:
        my_win_rate_starting_first = round(200 * my_win_rates[WINS, STARTING_FIRST] / matches, 3)
        my_win_rate_starting_second = round(200 * my_win_rates[WINS, STARTING_SECOND] / matches, 3)
        opponent_win_rate_starting_first = round(100 - my_win_rate_starting_second, 3)
        opponent_win_rate_starting_second = round(100 - my_win_rate_starting_first, 3)
        # win_rate_starting_first = 200 * my_win_rates[WINS, STARTING_FIRST] / matches
        # win_rate_starting_second = 200 * my_win_rates[WINS, STARTING_SECOND] / matches
        print(f'\n{STRATEGIES[indices[PLAYER1]]} win rate: {my_win_rate}%')
        print(f'{STRATEGIES[indices[PLAYER1]]} win rate starting first: {my_win_rate_starting_first}%')
        print(f'{STRATEGIES[indices[PLAYER1]]} win rate starting second: {my_win_rate_starting_second}%')
        print(f'\n{STRATEGIES[indices[PLAYER2]]} win rate: {opponent_win_rate}%')
        print(f'{STRATEGIES[indices[PLAYER2]]} win rate starting first: {opponent_win_rate_starting_first}%')
        print(f'{STRATEGIES[indices[PLAYER2]]} win rate starting second: {opponent_win_rate_starting_second}%')
        # print(f'\nprobability of winning when starting first: {win_rate_starting_first}%')
        # print(f'probability of winning when starting second: {win_rate_starting_second}%\n')
        return [my_win_rates, my_win_rate_starting_first, my_win_rate_starting_second], \
            [opponent_win_rate, opponent_win_rate_starting_first, opponent_win_rate_starting_second]#, \
            # [win_rate_starting_first, win_rate_starting_second]
    return my_win_rate > 50, opponent_win_rate > 50, sum(my_win_rates[WINS, :]), \
        my_win_rates[WINS, STARTING_FIRST], my_win_rates[WINS, STARTING_SECOND]


def get_info(state: Nim) -> dict:
    info = dict()
    # returns a list of (rows index, amount of objects to remove)
    info["possible_moves"] = [
        (r, o) for r, c in enumerate(state.get_rows) for o in range(1, c + 1)
        if state.get_k is None or o <= state.get_k
    ]
    info["shortest_row"] = min((x for x in enumerate(state.get_rows)
                                if x[1] > 0), key=lambda y: y[1])[0]
    info["longest_row"] = max((x for x in enumerate(state.get_rows)),
                              key=lambda y: y[1])[0]
    info["nim_sum"] = nim_sum(state)
    info["remaining rows"] = sum([int(x > 0) for x in state.get_rows])
    info["rows with more than 1"] = sum([int(x > 1) for x in state.get_rows])
    info["rows with 1"] = sum([int(x == 1) for x in state.get_rows])
    info["rows with 0"] = sum([int(x == 0) for x in state.get_rows])
    brute_force = []
    p_moves = info["possible_moves"]
    for m in p_moves:
        tmp = deepcopy(state)
        tmp.nimming(m)
        brute_force.append((m, nim_sum(tmp)))
    info["brute_force"] = brute_force
    return info


def run_tournament(strategies, k, matches):
    global_win_rates = np.zeros((4, len(strategies)))
    for i in range(len(strategies) - 1):
        for j in range(i + 1, len(strategies)):
            w1, w2, w3, w4, w5 = evaluate(strategies, k, matches, (i, j), tournament=True)
            global_win_rates[0, i] += w1  # % defeated opponents
            global_win_rates[0, j] += w2
            global_win_rates[1, i] += w3  # % games won
            global_win_rates[1, j] += matches - w3
            global_win_rates[2, i] += w4  # % games won starting first
            global_win_rates[2, j] += (matches / 2) - w5
            global_win_rates[3, i] += w5  # % games won starting second
            global_win_rates[3, j] += (matches / 2) - w4
        print(f'{STRATEGIES[i]}: {round(100 * global_win_rates[0, i] / (len(strategies) - 1), 3)}%',
              f'{round(100 * global_win_rates[1, i] / (matches * (len(strategies) - 1)), 3)}',
              f'\t\t{round(100 * global_win_rates[2, i] / ((matches / 2) * (len(strategies) - 1)), 3)}',
              f'{round(100 * global_win_rates[3, i] / ((matches / 2) * (len(strategies) - 1)), 3)}')
    print(f'{STRATEGIES[-1]}: {round(100 * global_win_rates[0, -1] / (len(strategies) - 1), 3)}%',
          f'{round(100 * global_win_rates[1, -1] / (matches * (len(strategies) - 1)), 3)}',
          f'\t\t{round(100 * global_win_rates[2, -1] / ((matches / 2) * (len(strategies) - 1)), 3)}',
          f'{round(100 * global_win_rates[3, -1] / ((matches / 2) * (len(strategies) - 1)), 3)}')
    global_win_rates = 100 * global_win_rates / (len(strategies) - 1)
    return global_win_rates


def nim_sum(state: Nim) -> int:
    *_, result = accumulate(state.get_rows, xor)
    return result

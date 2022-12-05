import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from game_utilities import Nim, get_info
from strategies.strategy_utilities import random
from strategies.strategy_utilities import PACIFIST, VIGILANT, AGGRESSIVE, ROWS, OBJECTS, ARRAY
from strategies.strategy_utilities import finishing_or_forced_move, generate_difference
from game_utilities import np
from game_utilities import PLAYER1, PLAYER2
# from math import ceil

# all p's are float and between [0, 1]


def s_pure_random(state: Nim, p) -> tuple:
    all_possibilities = [r for r, c in enumerate(state.get_rows) if c > 0]
    p1 = all_possibilities[:len(all_possibilities)//2]
    p2 = all_possibilities[len(all_possibilities)//2:]
    p_final = [p1, p2]
    index = np.random.choice(2, 1, [p, 1 - p])
    row = random.choice(p_final[index])
    num_objects = random.randint(1, state.get_rows[row])
    return row, num_objects


def s_gabriele(state: Nim, p: float) -> tuple:
    """Picks always the maximum possible number of objects in the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.get_rows) for o in range(1, c + 1)]
    return max(possible_moves, key=lambda m: ((1 if random.random() > p else -1) * m[0], m[1]))


def s_spreader(state: Nim, p: float) -> tuple:
    """takes 1 objects from all rows, it doesn't care of clearing rows unless it is forced to or if it is the move to
    win the game"""
    choices = [i for i in range(state.get_nrows)
               if state.get_rows[i] == state.get_original_rows[i] and state.get_rows[i] > 1]
    if len(choices) == 0:
        choices = [np.argmax(state.get_rows)]
    t_row = random.choice(choices)
    return t_row, state.get_rows[t_row] if finishing_or_forced_move(state) else max(1, (state.get_rows[t_row] - 1) * p)


def s_nimsum_little_brother(state: Nim, p: float) -> tuple:
    """nim-sum strategy but it doesn't use the original strategy until the very end. When it doesn't do this it tries to
    reach the optimal situation for the actual min-sum"""
    info = get_info(state)
    if info["rows with more than 1"] == 1 and info["rows with 1"] % 2 == 0:  # trigger
        t_row = np.argmax(state.get_rows)
        return t_row, state.get_rows[t_row]
    choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 1]  # setup
    if len(choices) == 0:
        choices = [i for i in range(state.get_nrows) if state.get_rows[i] == 1]
    t_row = random.choice(choices)
    t_amount = max(1, (state.get_rows[t_row] - 1) * p)  # p affect speed at reaching optimal situation for nim-sum
    return t_row, t_amount


def s_divergent(state, p: float):
    """each turn it either takes 1 object from a row having more than 1 objects or completely clears one row"""
    personality = AGGRESSIVE if finishing_or_forced_move(state) else np.random.choice([PACIFIST, AGGRESSIVE], 1, [p, 1 - p])
    choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 1]
    if personality == AGGRESSIVE or len(choices) == 0:
        choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 0]
    t_row = random.choice(choices)
    return t_row, 1 if personality == PACIFIST else state.get_rows[t_row]
# "MIRRORER" FAMILY ----------------------------------------------------------------------------------------------------


def s_the_reversed_mirrorer(state: Nim, reverse_mirror_flags: tuple) -> tuple:
    """What the opponent takes in a row, this strategy leaves in a row"""
    opponent_clear_flag = opponent_clear_flag_o = reverse_mirror_flags[ROWS] - get_info(state)["remaining rows"]
    difference = generate_difference(reverse_mirror_flags[ARRAY], state.get_rows)
    original_rows = [int(x) for x in state.get_rows]
    state.set_rows(original_rows)
    changed_row_index = np.argmax(difference)
    my_clear_flag = my_clear_flag_o = int(sum(difference) == 1)
    changing_factor = max(difference[changed_row_index], 1)
    if opponent_clear_flag + my_clear_flag == 2:
        if bool(np.random.choice([PLAYER1, PLAYER2], 1, [p, 1 - p])):
            opponent_clear_flag = 0
    if bool(opponent_clear_flag):
        choices = [x for x in range(state.get_nrows) if state.get_rows[x] > 1]
        if len(choices) == 0:
            choices = [x for x in range(state.get_nrows) if state.get_rows[x] > 0]
    elif bool(my_clear_flag):
        choices = [x for x in range(state.get_nrows) if state.get_rows[x] > 0]
    else:
        choices = [x for x in range(state.get_nrows) if state.get_rows[x] > changing_factor + 1]
        if len(choices) == 0:
            choices = [x for x in range(state.get_nrows) if state.get_rows[x] > 1]
            if len(choices) == 0:
                choices = [x for x in range(state.get_nrows) if state.get_rows[x] > 0]
    t_row = random.choice(choices)
    if finishing_or_forced_move(state) or bool(my_clear_flag):
        t_amount = state.get_rows[t_row]
    elif bool(opponent_clear_flag):
        t_amount = 1
    else:
        t_amount = min(state.get_rows[t_row] - changing_factor, state.get_rows[t_row] - 1)
    n_difference = [0 for _ in range(state.get_nrows)]
    n_difference[t_row] += t_amount
    reverse_mirror_flags = [reverse_mirror_flags[ROWS] - opponent_clear_flag_o - my_clear_flag_o,
                            generate_difference(state.get_rows, n_difference)]
    original_rows = [int(x) for x in state.get_rows]
    state.set_rows(original_rows)
    return (t_row, t_amount), reverse_mirror_flags


def s_the_balancer(state: Nim, p: float) -> tuple:
    target = sorted(set(state.get_rows))
    if len(target) < p * state.get_nrows:
        can_balance = False
        choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 1]
        if len(choices) == 0:
            choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 0]
    else:
        can_balance = True
        target = target[-int(p * state.get_nrows)]
        choices = [i for i in range(state.get_nrows) if state.get_rows[i] > target]
    t_row = random.choice(choices)
    if finishing_or_forced_move(state):
        return t_row, state.get_rows[t_row]
    return t_row, (state.get_rows[t_row] - target if can_balance else 1)

import random
import numpy as np
from utilities import Nim, get_info
from utilities import PLAYER1, PLAYER2
from typing import Callable

PACIFIST = 0
VIGILANT = 1
AGGRESSIVE = 2

ROWS = 0
OBJECTS = 1
ARRAY = 1

OPTIMAL_STRATEGY = 5
PURE_RANDOM = 6
GABRIELE = 7
MAKE_STRATEGY_1 = 8
MAKE_STRATEGY_5 = 9
MAKE_STRATEGY_9 = 10
DUMMY = 11
DIVERGENT = 0
DIVERGENT_CHALLENGER = 1
SPREADER = 2
AGGRESSIVE_SPREADER = 3
NIMSUM_LITTLE_BROTHER = 4
DIVERGENT_TRIPHASE = 12
THE_BALANCER = 13
THE_MIRRORER = 14
RANDOM_SPREADER = 15
THE_REVERSED_MIRRORER = 16


def optimal_strategy(state: Nim) -> tuple:  # benchmark
    data = get_info(state)
    return next((bf for bf in data["brute_force"] if bf[1] == 0),
                random.choice(data["brute_force"]))[0]


def dummy(state: Nim = None) -> tuple:  # benchmark
    return 0, 0


def pure_random(state: Nim) -> tuple:
    row = random.choice([r for r, c in enumerate(state.get_rows) if c > 0])
    num_objects = random.randint(1, state.get_rows[row])
    return row, num_objects


def gabriele(state: Nim) -> tuple:
    """Picks always the maximum possible number of objects in the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.get_rows) for o in range(1, c + 1)]
    return max(possible_moves, key=lambda m: (-m[0], m[1]))


def spreader(state: Nim) -> tuple:
    """takes 1 objects from all rows, it doesn't care of clearing rows unless it is forced to or if it is the move to
    win the game"""
    choices = [i for i in range(state.get_nrows)
               if state.get_rows[i] == state.get_original_rows[i] and state.get_rows[i] > 1]
    if len(choices) == 0:
        choices = [np.argmax(state.get_rows)]
    t_row = random.choice(choices)
    return t_row, state.get_rows[t_row] if finishing_or_forced_move(state) else 1


def random_spreader(state: Nim):
    choices = [i for i in range(state.get_nrows)
               if state.get_rows[i] == state.get_original_rows[i] and state.get_rows[i] > 1]
    if len(choices) == 0:
        choices = [np.argmax(state.get_rows)]
    t_row = random.choice(choices)
    return t_row, state.get_rows[t_row] if finishing_or_forced_move(state) else random.randint(1, state.get_rows[
        t_row] - 1)


def aggressive_spreader(state: Nim) -> tuple:
    """same as before but it normally takes (all - 1) objects form a row each turn unless forced to, or it is the move
    to win the game (in those cases it clears the entire row)"""
    choices = [i for i in range(state.get_nrows) if
               state.get_rows[i] == state.get_original_rows[i] and state.get_rows[i] > 0]
    if len(choices) == 0:
        choices = [np.argmax(state.get_rows)]
    t_row = random.choice(choices)
    t_amount = max(1, state.get_rows[t_row] - 1)
    return t_row, state.get_rows[t_row] if finishing_or_forced_move(state) else t_amount


def nimsum_little_brother(state: Nim) -> tuple:
    """nim-sum strategy but it doesn't use the original strategy until the very end. When it doesn't do this it tries to
    reach the optimal situation for the actual min-sum"""
    info = get_info(state)
    if info["rows with more than 1"] == 1 and info["rows with 1"] % 2 == 0:  # trigger
        t_row = np.argmax(state.get_rows)[0]
        return t_row, state.get_rows[t_row]
    choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 1]  # setup
    if len(choices) == 0:
        choices = [i for i in range(state.get_nrows) if state.get_rows[i] == 1]
    t_row = random.choice(choices)
    t_amount = max(1, state.get_rows[t_row] - 1)
    return t_row, t_amount


def divergent(state):
    """each turn it either takes 1 object from a row having more than 1 objects or completely clears one row"""
    personality = AGGRESSIVE if finishing_or_forced_move(state) else random.choice([PACIFIST, AGGRESSIVE])
    choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 1]
    if personality == AGGRESSIVE or len(choices) == 0:
        choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 0]
    t_row = random.choice(choices)
    return t_row, 1 if personality == PACIFIST else state.get_rows[t_row]


def divergent_challenger(state):
    """same as before but during its aggressive stance, it always clears the row with the most objects"""
    personality = AGGRESSIVE if finishing_or_forced_move(state) else random.choice([PACIFIST, AGGRESSIVE])
    choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 1]
    if personality == PACIFIST and len(choices) == 0:
        choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 0]
    elif personality == AGGRESSIVE:
        choices = [np.argmax(state.get_rows)]
    t_row = random.choice(choices)
    return t_row, 1 if personality == PACIFIST else state.get_rows[t_row]


def divergent_triphase(state):
    """same as the original "divergent" strategy but in this case it also has a third state in which it removes a random
    amount of objects in such a way that it never clears a row"""
    personality = AGGRESSIVE if finishing_or_forced_move(state) else random.choice([PACIFIST, VIGILANT, AGGRESSIVE])
    choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 1]
    if personality == AGGRESSIVE or len(choices) == 0:
        choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 0]
    t_row = random.choice(choices)
    if personality == PACIFIST:
        return t_row, 1
    elif personality == VIGILANT:
        return t_row, max(1, state.get_rows[t_row] // 2)
    else:
        return t_row, state.get_rows[t_row]


def the_mirrorer(state: Nim, mirror_flags: tuple) -> tuple:
    """It tries to mirror as good as it can the opponent's moves"""
    objects_removed_by_opponent = mirror_flags[OBJECTS] - sum(state.get_rows)
    my_clear_flag = opponent_clear_flag = mirror_flags[ROWS] - get_info(state)["remaining rows"]
    if bool(opponent_clear_flag):
        choices = [x for x in range(state.get_nrows) if state.get_rows[x] ==
                   objects_removed_by_opponent and state.get_rows[x] > 0]
        if len(choices) == 0:
            choices = [x for x in range(state.get_nrows) if state.get_rows[x] > 0]
    else:
        choices = [x for x in range(state.get_nrows) if state.get_rows[x] > max(1, objects_removed_by_opponent)]
        if len(choices) == 0:
            choices = [x for x in range(state.get_nrows) if state.get_rows[x] > 1]
            my_clear_flag = 0.5
            if len(choices) == 0:
                choices = [x for x in range(state.get_nrows) if state.get_rows[x] > 0]
    t_row = random.choice(choices)
    if bool(opponent_clear_flag) or finishing_or_forced_move(state) or bool(my_clear_flag == 1):
        t_amount = state.get_rows[t_row]
    elif my_clear_flag == 0.5:
        t_amount = state.get_rows[t_row] - 1
    else:
        t_amount = max(1, objects_removed_by_opponent)
    mirror_flags = [mirror_flags[ROWS] - opponent_clear_flag - my_clear_flag,
                    mirror_flags[OBJECTS] - t_amount - objects_removed_by_opponent]
    return (t_row, t_amount), mirror_flags


def the_reversed_mirrorer(state: Nim, reverse_mirror_flags: tuple) -> tuple:
    """What the opponent takes in a row, this strategy leaves in a row"""
    opponent_clear_flag = opponent_clear_flag_o = reverse_mirror_flags[ROWS] - get_info(state)["remaining rows"]
    difference = generate_difference(reverse_mirror_flags[ARRAY], state.get_rows)
    original_rows = [int(x) for x in state.get_rows]
    state.set_rows(original_rows)
    changed_row_index = np.argmax(difference)
    my_clear_flag = my_clear_flag_o = int(sum(difference) == 1)
    changing_factor = max(difference[changed_row_index], 1)
    if opponent_clear_flag + my_clear_flag == 2:
        if bool(random.choice([PLAYER1, PLAYER2])):
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


def the_balancer(state: Nim) -> tuple:
    target = sorted(set(state.get_rows))
    if len(target) < 2:
        can_balance = False
        choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 1]
        if len(choices) == 0:
            choices = [i for i in range(state.get_nrows) if state.get_rows[i] > 0]
    else:
        can_balance = True
        target = target[-2]
        choices = [i for i in range(state.get_nrows) if state.get_rows[i] > target]
    t_row = random.choice(choices)
    if finishing_or_forced_move(state):
        return t_row, state.get_rows[t_row]
    return t_row, (state.get_rows[t_row] - target if can_balance else 1)


def make_strategy(p: float) -> Callable:
    def evolvable(state: Nim) -> tuple:
        data = get_info(state)
        if random.random() < p:
            ply = (data["shortest_row"], random.randint(1, state.get_rows[data["shortest_row"]]))
        else:
            ply = (data["longest_row"], random.randint(1, state.get_rows[data["longest_row"]]))
        return ply
    return evolvable


def finishing_or_forced_move(state):
    return (get_info(state)["remaining rows"] == 1 and sum(state.get_rows) > 1) or \
        get_info(state)["rows with more than 1"] == 0


def generate_difference(list1, list2):
    result = []
    for i in range(len(list1)):
        result.append(list1[i] - list2[i])
    return result

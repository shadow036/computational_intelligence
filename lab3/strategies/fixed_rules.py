import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from game_utilities import Nim, get_info
from strategies.strategy_utilities import random
from strategies.strategy_utilities import PACIFIST, VIGILANT, AGGRESSIVE, ROWS, OBJECTS
from strategies.strategy_utilities import analyze_situation, killer_instinct
from game_utilities import np
from math import ceil


def optimal_strategy(state: Nim) -> tuple:  # benchmark
    data = get_info(state)
    return next((bf for bf in data["brute_force"] if bf[1] == 0),
                random.choice(data["brute_force"]))[0]


def dummy(state: Nim = None) -> tuple:  # benchmark
    return 0, 0   # it doesn't do anything (the state remains the same)


def pure_random(state: Nim) -> tuple:
    """already present"""
    row = random.choice([r for r, c in enumerate(state.return_rows) if c > 0])
    num_objects = random.randint(1, state.return_rows[row])
    return row, num_objects


def gabriele(state: Nim) -> tuple:
    """Picks always the maximum possible number of objects in the lowest row"""
    possible_moves = [(r, o) for r, c in enumerate(state.return_rows) for o in range(1, c + 1)]
    return max(possible_moves, key=lambda m: (-m[0], m[1]))


def spreader(state: Nim) -> tuple:
    """takes 1 objects from all rows, it doesn't care of clearing rows unless it is forced to or if it is the move to
    win the game"""
    choices = [i for i in range(state.return_nrows) if state.return_rows[i] == state.return_original_rows[i]]
    if len(choices) == 0:
        choices = [np.argmax(state.return_rows)]
    t_row = random.choice(choices)
    return t_row, state.return_rows[t_row] if killer_instinct(state) else 1


def aggressive_spreader(state: Nim) -> tuple:
    """same as before but it normally takes (all - 1) objects form a row each turn unless forced to or it is the move
    to win the game (in those cases it clears the entire row)"""
    choices = [i for i in range(state.return_nrows) if state.return_rows[i] == state.return_original_rows[i]]
    if len(choices) == 0:
        choices = [np.argmax(state.return_rows)]
    t_row = random.choice(choices)
    t_amount = max(1, state.return_rows[t_row] - 1)
    return t_row, state.return_rows[t_row] if killer_instinct(state) else t_amount


def nimsum_lil_brother(state: Nim) -> tuple:
    """nim-sum strategy but it doesn't use the original strategy until the very end. When it doesn't do this it tries to
    reach the optimal situation for the actual min-sum"""
    info = get_info(state)
    if info["rows with more than 1"] == 1 and info["rows with 1"] % 2 == 0:  # trigger
        t_row = np.argmax(state.return_rows)
        return t_row, state.return_rows[t_row]
    choices = [i for i in range(state.return_nrows) if state.return_rows[i] > 1]  # setup
    if len(choices) == 0:
        choices = [i for i in range(state.return_nrows) if state.return_rows[i] == 1]
    t_row = random.choice(choices)
    t_amount = max(1, state.return_rows[t_row] - 1)
    return t_row, t_amount


def hel(state):
    """each turn it either takes 1 object from a row having more than 1 objects or completely clears one row"""
    killer_instinct = get_info(state)["remaining rows"] == 1 and sum(state.return_rows) > 1
    personality = AGGRESSIVE if killer_instinct else random.choice([PACIFIST, AGGRESSIVE])
    choices = [i for i in range(state.return_nrows) if state.return_rows[i] > 1]
    if personality == AGGRESSIVE or len(choices) == 0:
        choices = [i for i in range(state.return_nrows) if state.return_rows[i] > 0]
    t_row = random.choice(choices)
    return t_row, 1 if personality == PACIFIST else state.return_rows[t_row]


def hel_challenger(state):
    """same as before but during its aggressive stance, it always clears the row with the most objects"""
    personality = AGGRESSIVE if killer_instinct(state) else random.choice([PACIFIST, AGGRESSIVE])
    choices = [i for i in range(state.return_nrows) if state.return_rows[i] > 1]
    if personality == PACIFIST and len(choices) == 0:
        choices = [i for i in range(state.return_nrows) if state.return_rows[i] > 0]
    elif personality == AGGRESSIVE:
        choices = [np.argmax(state.return_rows)]
    t_row = random.choice(choices)
    return t_row, 1 if personality == PACIFIST else state.return_rows[t_row]


def hel_triphase(state):
    """same as the original "hel" strategy but in this case it also has a third state in which it removes a random
    amount of objects in such a way that it never clears a row"""
    personality = AGGRESSIVE if killer_instinct(state) else random.choice([PACIFIST, VIGILANT, AGGRESSIVE])
    choices = [i for i in range(state.return_nrows) if state.return_rows[i] > 1]
    if personality == AGGRESSIVE or len(choices) == 0:
        choices = [i for i in range(state.return_nrows) if state.return_rows[i] > 0]
    t_row = random.choice(choices)
    if personality == PACIFIST:
        return t_row, 1
    elif personality == VIGILANT:
        t_amount = random.choice([i/10 for i in range(1, 10)])
        return t_row, max(min(ceil(t_amount * state.return_rows[t_row]), state.return_rows[t_row] - 1), 1)
    else:
        return t_row, state.return_rows[t_row]


def the_mirrorer(state: Nim) -> tuple:
    """It tries to mirror as good as it can the opponent's moves"""
    t_row, t_amount, flag = analyze_situation(state)
    state.set_mirror_flags((state.return_mirror_flags[ROWS] - int(flag), state.return_mirror_flags[OBJECTS] - t_amount))
    return t_row, t_amount


def the_balancer(state: Nim) -> tuple:
    target = sorted(set(state.return_rows))
    if len(target) < 2:
        can_balance = False
        choices = [i for i in range(state.return_nrows) if state.return_rows[i] > 1]
        if len(choices) == 0:
            choices = [i for i in range(state.return_nrows) if state.return_rows[i] > 0]
    else:
        can_balance = True
        target = target[-2]
        choices = [i for i in range(state.return_nrows) if state.return_rows[i] > target]
    t_row = random.choice(choices)
    if killer_instinct(state):
        return t_row, state.return_rows[t_row]
    return t_row, (state.return_rows[t_row] - target if can_balance else 1)

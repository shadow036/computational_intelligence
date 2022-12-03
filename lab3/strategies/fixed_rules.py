from game_utilities import Nim, get_info
from strategies.strategy_utilities import random
from strategies.strategy_utilities import PACIFIST, VIGILANT, AGGRESSIVE
from strategies.strategy_utilities import analyze_situation, set_new_situation
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
    # takes 1 objects from all rows, it doesn't care of clearing rows
    choices = [i for i in range(state.return_nrows) if state.return_rows[i] == state.return_original_rows[i]]
    if len(choices) == 0:
        choices = [np.argmax(state.return_rows)]
    t_row = random.choices(choices)[0]
    t_amount = random.choices([0.1 * j for j in range(6)])[0]
    return t_row, ceil(t_amount * state.return_rows[t_row])


def aggressive_spreader(state: Nim) -> tuple:
    """same as before but it takes (all - 1) objects form a row each turn. It never clears them during its first visit
    on that row unless necessary"""
    choices = [i for i in range(state.return_nrows) if state.return_rows[i] == state.return_original_rows[i]]
    if len(choices) == 0:
        choices = [np.argmax(state.return_rows)]
    t_row = random.choices(choices)[0]
    t_amount = (max(1, state.return_rows[t_row] - 1))
    return t_row, t_amount


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
    t_row = random.choices(choices)[0]
    t_amount = max(1, state.return_rows[t_row] - 1)
    return t_row, t_amount


def hel(state):
    """each turn it either takes 1 object from a row having more than 1 objects or completely clears one row"""
    personality = random.choices([PACIFIST, AGGRESSIVE])
    if personality == PACIFIST:
        choices = [i for i in range(state.return_nrows) if state.return_rows[i] > 1]
    else:
        choices = [i for i in range(state.return_nrows) if state.return_rows[i] > 0]
    t_row = random.choices(choices)[0]
    return t_row, 1 if personality == PACIFIST else state.return_rows[t_row]


def hel_challenger(state):
    """same as before but during its aggressive stance, it always clears the row with the most objects"""
    personality = random.choices([PACIFIST, AGGRESSIVE])
    if personality == PACIFIST:
        choices = [i for i in range(state.return_nrows) if state.return_rows[i] > 1]
    else:
        choices = [np.argmax(state.return_rows)]
    t_row = random.choices(choices)[0]
    return t_row, 1 if personality == PACIFIST else state.return_rows[t_row]


def hel_triphase(state):
    """same as the original "hel" strategy but in this case it also has a third state in which it removes a random
    amount of objects in such a way that it never clears a row"""
    personality = random.choices([PACIFIST, VIGILANT, AGGRESSIVE])
    if personality == PACIFIST or personality == VIGILANT:
        choices = [i for i in range(state.return_nrows) if state.return_rows[i] > 1]  # doesn't clear a row for sure
    else:
        choices = [np.argmax(state.return_rows)]
    t_row = random.choices(choices)[0]
    if personality == PACIFIST:
        return t_row, 1
    elif personality == VIGILANT:
        t_amount = random.choices([i/10 for i in range(1, 10)])
        return t_row, min(ceil(t_amount * state.return_rows[t_row]), state.return_rows[t_row] - 1)
        # between pacifist and aggressive stance
    else:
        return t_row, state.return_rows[t_row]


def semi_self_adapter(state: Nim) -> tuple:
    """deterministic behaviour. "Semi" because it still uses fixed rules"""
    # todo
    analyze_situation(state)
    set_new_situation((sum(state.return_rows), sum([x for x in state.return_rows if x > 0])))
    return 0, 0

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from game_utilities import Callable
from game_utilities import Nim, get_info, random


EARLY_GAME = 0
MID_GAME = 1
LATE_GAME = 2

# 'divergent', 'divergent_challenger', 'divergent_triphase' utility constants
PACIFIST = 0
VIGILANT = 1
AGGRESSIVE = 2

ROWS = 0
OBJECTS = 1
ARRAY = 1


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


def make_substrategy(base: Callable, type: int, p: float) -> Callable:
    def new_substrategy(state: Nim) -> Callable:
        return base(state, p)
    return new_substrategy, type


def substrategies_mutation(type, old_p, base):
    return make_substrategy(base, type, random.choice([
        min(1, old_p + random.random()),
        max(0, old_p - random.random())])
                            )

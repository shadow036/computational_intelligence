import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from game_utilities import Callable
from game_utilities import Nim, get_info, random


EARLY_GAME = 0
MID_GAME = 1
LATE_GAME = 2

# 'hel', 'hel_challenger', 'hel_triphase' utility constants
PACIFIST = 0
VIGILANT = 1
AGGRESSIVE = 2

ROWS = 0
OBJECTS = 1

def make_strategy(p: float) -> Callable:
    def evolvable(state: Nim) -> tuple:
        data = get_info(state)
        if random.random() < p:
            ply = (data["shortest_row"], random.randint(1, state.return_rows[data["shortest_row"]]))
        else:
            ply = (data["longest_row"], random.randint(1, state.return_rows[data["longest_row"]]))
        return ply
    return evolvable


def analyze_situation(state):
    objects_removed_by_opponent = state.return_mirror_flags[OBJECTS] - sum(state.return_rows)
    row_cleared_by_opponent = bool(state.return_mirror_flags[ROWS] - get_info(state)["remaining rows"] > 0)
    flag = False
    if row_cleared_by_opponent:
        choices = [x for x in range(state.return_nrows) if 0 < state.return_rows[x] == objects_removed_by_opponent]
        if len(choices) == 0:
            choices = [x for x in range(state.return_nrows) if state.return_rows[x] > 0]
    else:
        choices = [x for x in range(state.return_nrows) if state.return_rows[x] > max(1, objects_removed_by_opponent)]
        if len(choices) == 0:
            choices = [x for x in range(state.return_nrows) if state.return_rows[x] > 1]
            if len(choices) == 0:
                choices = [x for x in range(state.return_nrows) if state.return_rows[x] > 0]
                flag = True
    t_row = random.choice(choices)
    if row_cleared_by_opponent or killer_instinct(state):
        return t_row, state.return_rows[t_row], True
    else:
        return t_row, max(1, state.return_mirror_flags[OBJECTS] - sum(state.return_rows)), flag


def killer_instinct(state):
    return get_info(state)["remaining rows"] == 1 and sum(state.return_rows) > 1

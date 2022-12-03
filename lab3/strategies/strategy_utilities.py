from game_utilities import Callable
from game_utilities import Nim, get_info, random


EARLY_GAME = 0
MID_GAME = 1
LATE_GAME = 2

# 'hel', 'hel_challenger', 'hel_triphase' utility constants
PACIFIST = 0
VIGILANT = 1
AGGRESSIVE = 2

# strategies already present
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
SEMI_SELF_ADAPTER = 13
# used for the "analyze situation" function and the "semi_self_adapter" strategy
SEMI_EVOLUTION_FLAGS = 0, 0


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
    objects_removed_by_opponent = SEMI_EVOLUTION_FLAGS[0] - sum(state.return_rows)
    row_cleared_by_opponent = bool(SEMI_EVOLUTION_FLAGS[1] - sum([x for x in state.return_rows if x > 0]))
    if objects_removed_by_opponent > state.return_k or \
            (row_cleared_by_opponent and objects_removed_by_opponent > state.return_k/10):
        """opponent is playing aggressively"""

        pass
    else:
        """opponent is playing casually"""
        pass


def set_new_situation(n_situation):
    global SEMI_EVOLUTION_FLAGS
    SEMI_EVOLUTION_FLAGS = n_situation

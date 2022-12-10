from math import inf

MY_TURN = 1
OPPONENT_TURN = 0


def local_nimming(current_state, possible_actions):
    return [(current_state[index] - possible_actions[1] if index == possible_actions[0] else current_state[index])
            for index in range(len(current_state))]


class Node:
    def __init__(self, state, turn, parent=None):
        self.state = state
        self.turn = turn
        self.parent = parent
        self.rewards = []
        self.best_reward = []
        self.n_children = None
        self.find_actions_and_states()

    def find_actions_and_states(self):
        for row in range(len(self.state)):
            for taken_elements in range(1, self.state[row] + 1):
                possible_action = (row, taken_elements)
                self.rewards.append(
                    [possible_action,
                     Node(local_nimming(self.state, possible_action), 1 - self.turn, parent=self),
                     None
                     ])
        self.n_children = len(self.rewards)

    def propagate_backwards(self):
        if self.n_children == 0:
            self.best_reward = (2 * self.turn) - 1
        elif self.n_children != sum(int(r[2] is not None) for r in self.rewards):
            known_reward_children = [c[1] for c in self.rewards if c[2] is not None]
            all_children = [c[1] for c in self.rewards]
            for c in [c for c in all_children if c not in known_reward_children]:
                c.propagate_backwards()
            self.best_reward = max(self.rewards, key=lambda reward: (reward[2] if reward[2] is not None else inf))[2]\
                if bool(MY_TURN) else min(self.rewards, key=lambda reward: (reward[2] if reward[2] is not None else -inf))[2]
        if self.parent is not None:
            self.parent.add_child_reward((self, self.best_reward))

    def add_child_reward(self, child_reward):
        for c in self.rewards:
            if c[1] == child_reward[0]:
                c[2] = child_reward[1]
                break


def alpha_beta_pruning(Node):
    pass

from math import inf
import numpy as np

MY_TURN = 1
OPPONENT_TURN = 0

MINMAX = 25


def local_nimming(current_state, possible_actions):
    return [(current_state[index] - possible_actions[1] if index == possible_actions[0] else current_state[index])
            for index in range(len(current_state))]


class MinMax:
    def __init__(self, n_rows, starting_player):
        self.minmax = Node([(2 * row) + 1 for row in range(n_rows)], OPPONENT_TURN, OPPONENT_TURN)
        self.starting_player = starting_player
        self.current_node = self.minmax
        self.old_state = self.minmax.state
        self.n_rows = n_rows

    def add_actions_nodesRewards(self):
        self.minmax.propagate_backwards()

    def play(self, nim):
        opponent_move = [abs(self.old_state[i] - nim.get_rows[i]) for i in range(self.n_rows)]
        opponent_ply = (np.argmax(opponent_move), max(opponent_move))
        if opponent_ply != (0, 0):
            self.follow_changes(opponent_ply)
        my_ply = self.get_best_action()
        self.follow_changes(my_ply)
        self.old_state = self.current_node.state
        return my_ply

    def follow_changes(self, action):
        self.current_node = self.current_node.actions_nodesRewards[action][0]

    def reset_minmax(self):
        self.current_node = self.minmax
        self.old_state = self.minmax.state

    def visualize_tree(self):
        self.minmax.visualize_node()

    def get_best_action(self):
        return self.current_node.best_action


class Node:
    def __init__(self, state, turn, starting_player, parent=None):
        self.state = state
        self.turn = turn
        self.parent = parent
        self.actions_nodesRewards = {}  # {action: (child, reward)} dictionary containing the info for all possible actions in this node
        self.best_action = ()    # (action, reward): best choice in this node
        self.n_children = None
        self.starting_player = starting_player
        self.find_actions_and_states()

    def find_actions_and_states(self):
        for row in range(len(self.state)):
            for taken_elements in range(1, self.state[row] + 1):
                possible_action = (row, taken_elements)
                new_state = local_nimming(self.state, possible_action)
                self.actions_nodesRewards[possible_action] = (
                    Node(new_state, 1 - self.turn, self.starting_player, parent=self),
                    None
                )
        self.n_children = len(self.actions_nodesRewards)

    def propagate_backwards(self):
        self.best_action = None
        reward = None
        if self.n_children == 0:
            reward = (2 * self.turn) - 1
        elif self.n_children != sum([int(self.actions_nodesRewards[key][1] is not None) for key
                                     in self.actions_nodesRewards]):
            known_reward_children = [self.actions_nodesRewards[key][0] for key in self.actions_nodesRewards
                                     if self.actions_nodesRewards[key][1] is not None]
            all_children = [self.actions_nodesRewards[key][0] for key in self.actions_nodesRewards]
            for c in [c for c in all_children if c not in known_reward_children]:
                c.propagate_backwards()
            target = (
                max(self.actions_nodesRewards, key=lambda key: (self.actions_nodesRewards[key][1] if
                                                                 self.actions_nodesRewards[key][1]
                                                                 is not None else -inf))
            if (self.parent is None and self.starting_player == MY_TURN) or (self.parent is not None
                                                                             and self.parent.turn == MY_TURN)
                else min(
                    self.actions_nodesRewards, key=lambda key: (self.actions_nodesRewards[key][1] if
                                                                self.actions_nodesRewards[key][1] is not None else inf)))
            self.best_action = target
            reward = self.actions_nodesRewards[target][1]
        if self.parent is not None:
            self.parent.add_child_reward((self, reward))

    def add_child_reward(self, child_reward):
        for key in self.actions_nodesRewards:
            if self.actions_nodesRewards[key][0] == child_reward[0]:
                self.actions_nodesRewards[key] = child_reward
                break

    def visualize_node(self):
        for c in self.actions_nodesRewards:
            print(f'{self.state} --[action = {c}, reward = {self.actions_nodesRewards[c][1]}]--> {self.actions_nodesRewards[c][0].state}')
        for c in self.actions_nodesRewards:
            self.actions_nodesRewards[c][0].visualize_node()

def alpha_beta_pruning(Node):
    pass

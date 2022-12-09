import numpy as np

LEARNING_RATE = 0.3
EXPLORATION_RATE = 0.2


class Agent:
    def __init__(self, n_rows, learning_rate=LEARNING_RATE, exploration_rate=EXPLORATION_RATE):
        self.actions_beliefs = initialize_beliefs(n_rows)
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate

    def get_beliefs(self):
        return self.actions_beliefs

    def get_learning_rate(self):
        return self.learning_rate

    def choose_best_action(self, possible_actions):
        best_action = None
        for possible_action in possible_actions:
            if best_action is None or self.actions_beliefs[possible_action] > best_action[1]:
                best_action = (possible_action, self.actions_beliefs[possible_action])
        return best_action[0]

    def learn(self):
        pass


def initialize_beliefs(n_rows):
    beliefs = {}
    for row_index in range(n_rows):
        for taken_elements_minus_1 in range((2 * row_index) + 1):
            beliefs[(row_index, taken_elements_minus_1)] = np.random.uniform(low=0.1)
    return beliefs


def get_possible_actions(environment, n_rows):
    possible_actions = []
    for row_index in range(n_rows):
        for elements_amount in range(environment[row_index]):
            possible_actions.append((row_index, elements_amount))
    return possible_actions

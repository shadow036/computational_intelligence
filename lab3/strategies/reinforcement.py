import numpy as np
from math import inf

LEARNING_RATE = 0.5
EXPLORATION_RATE = 0.2

REINFORCEMENT = 24


class Agent:
    def __init__(self, n_rows, learning_rate=LEARNING_RATE, exploration_rate=EXPLORATION_RATE):
        self.state_beliefs = initialize_beliefs([(2 * row) + 1 for row in range(n_rows)], n_rows)
        self.learning_rate = learning_rate
        self.exploration_rate = exploration_rate
        self.state_list = []
        self.n_rows = n_rows

    def get_beliefs(self):
        return self.state_beliefs

    def get_exploration_rate(self):
        return self.exploration_rate

    def add_state_list(self, state, reward):
        self.state_list.append((state, reward))

    def reset_state_list(self):
        self.state_list = []

    def learn(self):
        outcome = self.state_list[-1][1]
        penalty_sum = 0
        counter = 0
        for a in self.state_list[::-1]:
            self.state_beliefs[a[0]] = self.state_beliefs[a[0]] + \
                                       self.learning_rate * ((outcome if counter == 0 else penalty_sum) -
                                                             self.state_beliefs[a[0]])
            penalty_sum += a[1]
            counter += 1

    def play(self, environment):
        possible_actions = get_possible_actions(environment.get_rows, self.n_rows)
        best_action = choose_best_action(possible_actions, environment, self)
        return best_action[0], best_action[1] + 1

    def decrease_exploration_rate(self, amount):
        self.exploration_rate -= amount

    def reset_exploration_rate(self, amount):
        self.exploration_rate = amount


def choose_best_action(possible_actions, environment, agent):
    best_action = None
    for possible_action in possible_actions:
        belief = simulate_nimming(environment, possible_action, agent)
        new_state = environment.get_rows
        old_state = [(new_state[index] + possible_action[1] + 1 if index == possible_action[0] else new_state[index])
                     for index in range(environment.get_nrows)]
        environment.set_rows(old_state)
        if best_action is None or belief > best_action[1]:
            best_action = (possible_action, belief)
    return best_action[0]


def simulate_nimming(environment, action, agent):
    environment.nimming((action[0], action[1] + 1))
    return agent.get_beliefs()[make_hashable(environment.get_rows)]


def evaluate_state(new_state):
    if sum(new_state) % 2 == 0 and sum([int(e > 1) for e in new_state]) == 0:
        return 0
    if sum(new_state) % 2 == 1 and sum([int(e > 1) for e in new_state]) == 0:
        return -10
    return -1


def make_hashable(rows):
    string = ''
    for e in rows:
        string = string + ' ' + str(e)
    return string


def generate_dictionary(rows, n_rows, t_row, beliefs):
    if rows[t_row] == -1:
        return beliefs
    beliefs[make_hashable(rows)] = np.random.uniform(low=0.1)
    for t_row in range(t_row, n_rows):
        beliefs = generate_dictionary([rows[row] if row != t_row else rows[row] - 1 for row in range(n_rows)], n_rows,
                                      t_row, beliefs)
    return beliefs


def initialize_beliefs(rows, n_rows):
    beliefs = {}
    for t_row in range(n_rows):
        beliefs = generate_dictionary(rows, n_rows, t_row, beliefs)
    return beliefs


def get_possible_actions(environment, n_rows):
    possible_actions = []
    for row_index in range(n_rows):
        for elements_amount in range(environment[row_index]):
            possible_actions.append((row_index, elements_amount))
    return possible_actions


def show_learning_progress(new):
    progress = ''
    for step in range(0, 100, 1):
        if new > step:
            progress += '#'
        else:
            progress += '.'
    progress += f' {new}%'
    return progress

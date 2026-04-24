import random

class TrafficRL:
    def __init__(self):
        self.actions = [10, 20, 30]

    def get_action(self, state):
        # simple random decision
        return random.choice(self.actions)

    def update(self, state, action, reward, next_state):
        # simple update (no error)
        pass
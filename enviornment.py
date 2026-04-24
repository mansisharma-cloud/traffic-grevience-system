import random

class TrafficEnvironment:
    def __init__(self):
        self.vehicles = 0

    def reset(self):
        # start with random traffic
        self.vehicles = random.randint(0, 10)
        return self.vehicles

    def step(self, action):
        # action: 0 = short, 1 = medium, 2 = long green

        # cars passing based on signal time
        if action == 0:
            passed = 2
        elif action == 1:
            passed = 4
        else:
            passed = 6

        # new incoming cars
        incoming = random.randint(0, 3)

        # update traffic
        self.vehicles = self.vehicles + incoming - passed

        if self.vehicles < 0:
            self.vehicles = 0

        # reward → less vehicles is better
        reward = -self.vehicles

        return self.vehicles, reward
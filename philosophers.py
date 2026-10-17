import threading
import time
import random

# R - rest, T - think, E - eat, W - wait
states = ["R", "R", "R", "R", "R"]

# eat count for proving starvation
eat_count = [0, 0, 0, 0, 0]

# -1 = free, any other is ID of the philosopher
sticks = [-1, -1, -1, -1, -1]

class Philosopher(threading.Thread):
    def __init__(self, id_philosopher, name):
        super().__init__()
        self.id = id_philosopher
        self.name = name

        # end flag for automatic program closing
        self.daemon = True

    def run(self):
        # initialize philosopher process, starting from rest position
        states[self.id] = "R"
        time.sleep(random.random())

        while self.end:
            # making the philosopher wait for free chopstick
            states[self.id] = "W"
            time.sleep(1)

            # making the philosopher grab free stick and eat
            states[self.id] = "E"
            time.sleep(random.uniform(1, 4))
            eat_count[self.id] += 1

            # making the philosopher think after eating
            states[self.id] = "T"
            time.sleep(random.uniform(2, 5))
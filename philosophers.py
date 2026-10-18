import threading
import time
import random

# R - rest, T - think, E - eat, W - wait
states = ["R", "R", "R", "R", "R"]

# eat count for proving starvation
eat_count = [0, 0, 0, 0, 0]

# -1 = free, any other is ID of the philosopher
sticks = [-1, -1, -1, -1, -1]
# creatin mutexes to avoid acquiring a nonexistent stick by a philosopher
locked_sticks = [threading.Lock() for i in range(5)]

class Philosopher(threading.Thread):
    def __init__(self, id_philosopher, name, variant):
        super().__init__()
        self.id = id_philosopher
        self.name = name

        self.left_stick = self.id
        self.right_stick = (self.id + 1) % 5

        self.variant = variant

        # end flag for automatic program closing
        self.daemon = True

    def run(self):
        # initialize philosopher process, starting from rest position
        states[self.id] = "R"
        time.sleep(random.random())

        while self.daemon:
            # making the philosopher wait for free chopstick
            states[self.id] = "W"

            # trying to get left stick
            locked_sticks[self.left_stick].acquire()
            sticks[self.left_stick] = self.id

            # deadlock cause, longer delay means more chances for locking every stick simultaneously
            if self.variant == 1:
                time.sleep(0.1)
            elif self.variant == 2:
                time.sleep(1)

            # trying to get right stick
            locked_sticks[self.right_stick].acquire()
            sticks[self.right_stick] = self.id

            # making the philosopher grab free stick and eat
            states[self.id] = "E"
            time.sleep(random.uniform(1, 4))
            eat_count[self.id] += 1

            # freeing used sticks
            sticks[self.left_stick] = -1
            locked_sticks[self.left_stick].release()

            sticks[self.right_stick] = -1
            locked_sticks[self.right_stick].release()

            # making the philosopher think after eating
            states[self.id] = "T"
            time.sleep(random.uniform(2, 5))
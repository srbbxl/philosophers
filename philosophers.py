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

        # setting up stick indexes, % 5 so the last one wraps around to 0
        self.left_stick = self.id
        self.right_stick = (self.id + 1) % 5

        self.variant = variant

        # end flag for automatic program closing
        self.daemon = True

    def run(self):
        # initialize philosopher process, starting from rest position
        states[self.id] = "R"
        time.sleep(random.random())

        while True:
            # making the philosopher wait for free chopstick
            states[self.id] = "W"

            # variant 1 - correct, picking lower index first to avoid circular wait
            if self.variant == 1:

                first_stick = min(self.left_stick, self.right_stick)
                second_stick = max(self.left_stick, self.right_stick)

                # grabbing first stick
                locked_sticks[first_stick].acquire()
                sticks[first_stick] = self.id

                # grabbing second stick
                locked_sticks[second_stick].acquire()
                sticks[second_stick] = self.id

            # variant 2 - deadlock, everyone grabs left and waits
            elif self.variant == 2:

                # trying to get left stick
                locked_sticks[self.left_stick].acquire()
                sticks[self.left_stick] = self.id

                # delay so everyone grabs their left stick at the same time
                time.sleep(1)

                # trying to get right stick
                locked_sticks[self.right_stick].acquire()
                sticks[self.right_stick] = self.id

            # variant 3 - starvation, last philosopher is too polite
            elif self.variant == 3:
                if self.id == 4:
                    locked_sticks[self.left_stick].acquire()
                    sticks[self.left_stick] = self.id

                    # checking if right stick is free without blocking thread
                    if not locked_sticks[self.right_stick].acquire(blocking=False):

                        # right is taken so dropping left stick and waiting a bit
                        sticks[self.left_stick] = -1
                        locked_sticks[self.left_stick].release()

                        time.sleep(random.uniform(0.5, 1))
                        continue

                    sticks[self.right_stick] = self.id

                else:
                    # rest of philosophers just grab sticks normally
                    locked_sticks[self.left_stick].acquire()
                    sticks[self.left_stick] = self.id

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
            # shorter thinking time for others in variant 3 so id 4 starves faster
            if self.variant == 3 and self.id != 4:
                time.sleep(random.uniform(0.2, 0.8))
            else:
                time.sleep(random.uniform(2, 5))
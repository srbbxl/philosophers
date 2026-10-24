import time
from philosophers import Philosopher, states, eat_count, sticks

names = ["Dwalin", "Balin", "Thorin", "Fili", "Kili"]

# !!! VISUAL PART OF THIS PROJECT WAS MADE WITH AI HELP !!!


# ansi color codes for terminal output
GREEN = "\033[92m"   # eating
RED = "\033[91m"     # waiting
YELLOW = "\033[93m"  # thinking
CYAN = "\033[96m"    # resting
RESET = "\033[0m"    # default color

# helper function to wrap state letter in color
def get_colored_state(state):
    if state == "E":
        return f"{GREEN}E{RESET}"
    elif state == "W":
        return f"{RED}W{RESET}"
    elif state == "T":
        return f"{YELLOW}T{RESET}"
    else:
        return f"{CYAN}R{RESET}"

if __name__ == "__main__":
    philosophers = []
    # choosing simulation mode on start
    variant = int(input("choose a variant: (1 - correct, 2 - deadlock, 3 - starvation): "))

    # creating instances and running them one by one
    for i in range(5):
        f = Philosopher(i, names[i], variant)
        philosophers.append(f)
        f.start() # starting run() method

    try:
        while True:
            # clearing console using ansi escape code (avoids TERM variable error in ide)
            print("\033[H\033[J", end="")

            print("\n   state of table   ")
            # printing current status for each philosopher with colors
            for i in range(5):
                colored_st = get_colored_state(states[i])
                print(f"{i}: {names[i]:6} |  state: {colored_st} | times eaten: {eat_count[i]}")
            print(f"sticks: {sticks}")

            time.sleep(1)
    except KeyboardInterrupt:
        # stopping program with ctrl+c
        print("\nend")
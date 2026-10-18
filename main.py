import time

from philosophers import Philosopher, states, eat_count, sticks

names = ["Dwalin", "Balin", "Thorin", "Fili", "Kili"]

if __name__ == "__main__":
    philosophers = []
    variant = int(input("choose a variant: (1 - correct, 2 - deadlock, 3 - starvation): "))

    # creating instances and running them one by one
    for i in range(5):
        f = Philosopher(i, names[i], variant)
        philosophers.append(f)
        f.start() # starting run() method

    try:
        while True:
            print("\n   state of table   ")
            for i in range(5):
                print(f"{i}: {names[i]} |  state:{states[i]} | times eaten: {eat_count[i]}")
            print(f"sticks: {sticks}")


            time.sleep(1)
    except KeyboardInterrupt:
        print("end")
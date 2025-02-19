import sys
from ohbot import ohbot
import random
import time
import threading

ohbot.reset()

close_program = threading.Event()

def move_head():
    # Head is moved in a random direction
    ohbot.move(ohbot.HEADNOD, random.uniform(0, 10))
    ohbot.move(ohbot.HEADTURN, random.uniform(0, 10))

def blink_eyes():
    ohbot.move(ohbot.LIDBLINK, 0)
    ohbot.wait(0.4)
    ohbot.move(ohbot.LIDBLINK, 10)

def talk():
    # 1st Parameter is a text input that ohbot will say
    # 2nd parameter (False) means ohbot will continue moving while talking
    # 3rd parameter (True) means ohbot will lipsync to the text
    ohbot.say("Hello", False, True)

def close_eyes():
    ohbot.move(ohbot.LIDBLINK, 0)

def move_eyes():
    # Eyes are moved to random positions
    ohbot.move(ohbot.EYETURN, random.uniform(0, 10))
    ohbot.move(ohbot.EYETILT, random.uniform(0, 10))

def movement_sequence():
    move_head()
    ohbot.wait(1)
    blink_eyes()
    ohbot.wait(1)
    move_eyes()
    ohbot.wait(1)

def natural_head_movement():
    ohbot.move(ohbot.HEADNOD, random.uniform(4, 6))
    ohbot.move(ohbot.HEADTURN, random.uniform(4, 6))
    time.sleep(random.uniform(2, 5))
    ohbot.move(ohbot.HEADNOD, random.uniform(4, 6))
    ohbot.move(ohbot.HEADTURN, random.uniform(4, 6))
    time.sleep(random.uniform(2, 5))

def random_blink():
    ohbot.move(ohbot.LIDBLINK, 0)
    time.sleep(0.2)
    ohbot.move(ohbot.LIDBLINK, 10)
    # Random time until it blinks again
    time.sleep(random.uniform(3, 10))

def idle_animation_timer(seconds):
    start_time = time.time()
    while time.time() - start_time < seconds:
        natural_head_movement()
        random_blink()
'''
def idle_animation():
    print("Type exit to stop movement ")
    while True:
        natural_head_movement()
        random_blink()
        user_input = input()
        if user_input.lower() == "exit":
            shutdown()
            print("Ohbot has been shut down and is ready to be powered off.")
            break

'''
def idle_animation():
    print("Type exit to stop movement ")
    while not close_program.is_set():
        natural_head_movement()
        random_blink()

def check_for_input():
    while True:
        user_input = input()
        if user_input.lower() == "exit":
            shutdown()
            close_program.set()
            sys.exit(0)

def shutdown():
    # Shutdown ohbot
    ohbot.reset()
    ohbot.close()
    print("Ohbot has been shut down and is ready to be powered off.")


if __name__ == '__main__':
    #movement_sequence()
    #idle_animation_timer(60)  # Running tape for 60 seconds

    # Using threading so input can be taken while animations play
    animation_thread = threading.Thread(target=idle_animation)
    input_thread = threading.Thread(target=check_for_input)

    animation_thread.start()
    input_thread.start()

    input_thread.join()
    animation_thread.join()

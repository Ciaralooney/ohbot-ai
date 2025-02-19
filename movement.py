from ohbot import ohbot
import random
import time

ohbot.reset()

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
    # Using all these functions to make a sequence
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
    ohbot.move(ohbot.EYELIDBLINK, 0)
    time.sleep(0.2)
    ohbot.move(ohbot.EYELIDBLINK, 10)
    # Random time until it blinks again
    time.sleep(random.uniform(3, 10))

def idle_animation(seconds):
    start_time = time.time()
    while time.time() - start_time < seconds:
        natural_head_movement()
        random_blink()

if __name__ == '__main__':
    movement_sequence()
    # Running tape for 60 seconds
    idle_animation(60)
    ohbot.reset()
    ohbot.close()

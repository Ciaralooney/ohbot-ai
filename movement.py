from ohbot import ohbot
import random

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

if __name__ == '__main__':
    movement_sequence()
    ohbot.reset()
    ohbot.close()
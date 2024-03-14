from pyjoystick.sdl2 import Key, Joystick, run_event_loop
import gpiozero

print('Booting Grobot v0.0.3')
robot = gpiozero.Robot(left=(17,18), right=(27,22))

def print_add(joy):
    print('Added', joy)

def print_removed(joy):
    print('Removed', joy)

def key_received(key):
        if key.keytype != Key.HAT:
            return
        if key.value == Key.HAT_CENTERED:
            print('centered')
            robot.stop()
        if key.value == Key.HAT_UP:
            print('forward')
            robot.forward()
        elif key.value == Key.HAT_DOWN:
            print('down')
            robot.backward()
        if key.value == Key.HAT_LEFT:
            print('left')
            robot.left()
        elif key.value == Key.HAT_RIGHT:
            print('right')
            robot.right()

run_event_loop(print_add, print_removed, key_received)

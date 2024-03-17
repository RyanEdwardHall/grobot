from math import hypot
from pyjoystick.sdl2 import Key, Joystick, run_event_loop
import gpiozero

print('Booting Grobot v0.0.3')
robot = gpiozero.Robot(left=(17,18), right=(27,22))

def print_add(joy):
    print('Added', joy)

def print_removed(joy):
    print('Removed', joy)

vector = {'x': 0, 'y': 0}
def key_received(key):
    global vector
    if key.keytype == Key.AXIS and key.number in [0,1]:
        if key.number == 0:
            vector['x'] = key.value
        if key.number == 1:
            vector['y'] = key.value
        speed = hypot(vector['x'], vector['y'])
        clampedSpeed = sorted([-1, speed, 1])[1]
        leftMotorSpeed = clampedSpeed if vector['x'] >= 0 else clampedSpeed + vector['x']
        rightMotorSpeed = clampedSpeed if vector['x'] <= 0 else clampedSpeed - vector['x']
        if vector['y'] > 0:
            leftMotorSpeed *= -1
            rightMotorSpeed *= -1
        robot.left(leftMotorSpeed)
        robot.right(rightMotorSpeed)
        print('Left Motor: ', round(leftMotorSpeed, 3))
        print('Right Motor: ', round(rightMotorSpeed, 3))
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

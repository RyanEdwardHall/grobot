from math import hypot
from pyjoystick.sdl2 import Key, run_event_loop
import gpiozero

print('Booting Grobot: hold onto your sandwiches')

class Grobot:
    def __init__(self):
        self.move = gpiozero.Robot(left=(17,18), right=(27,22))
        self.actions = {
            Key.HAT_CENTERED: self.move.stop,
            Key.HAT_UP: self.move.forward,
            Key.HAT_DOWN: self.move.backward,
            Key.HAT_LEFT: self.move.left,
            Key.HAT_RIGHT: self.move.right
        }
        self.vector = {'x': 0, 'y': 0}
    def joy_added(joy):
        print('Joystick Found: ', joy)

    def joy_removed(joy):
        print('Joystick Removed: ', joy)

    def key_received(self, key):
        if key.keytype == Key.AXIS and key.number in [0,1]:
            direction = 'x' if key.number == 0 else 'y'
            self.vector[direction] = round(key.value, 4)
            speed = round(min(hypot(self.vector['x'], self.vector['y']), 1), 4)

            if self.vector['y'] != 0:
                move_func = self.move.forward if self.vector['y'] < 0 else self.move.backward
                curve = 'curve_left' if self.vector['x'] < 0 else 'curve_right'
                return move_func(speed, **{curve: abs(self.vector['x'])})
            else:
                return self.move.stop()
        action = self.actions.get(key.value)
        if action:
            return action();

g = Grobot()
run_event_loop(g.joy_added, g.joy_removed, g.key_received)

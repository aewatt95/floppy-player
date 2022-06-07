import OPi.GPIO as gpio
from Common import State

class LedManager:

    BLUE = 19
    RED = 23
    WHITE = 21


    def __init__(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(LedManager.RED, gpio.OUT)
        gpio.output(LedManager.RED, True)
        gpio.setup(LedManager.BLUE, gpio.OUT)
        gpio.output(LedManager.BLUE, True)
        gpio.setup(LedManager.WHITE, gpio.OUT)
        gpio.output(LedManager.WHITE, True)
        self.lastState = None
        pass

    def setOutput(self, white, red, blue):
        gpio.output(LedManager.BLUE, not blue)
        gpio.output(LedManager.RED, not red)
        gpio.output(LedManager.WHITE, not white)

    def handleState(self, state):
        if self.lastState != state:
            if state == State.RESET:
                self.setOutput(1, 0, 0)
            if state == State.IDLE:
                self.setOutput(1, 0, 0)
            if state == State.LOADING:
                self.setOutput(1, 0, 1)
            if state == State.PLAYING:
                self.setOutput(1, 0, 1)
            if state == State.END:
                self.setOutput(1, 0, 0)
            if state == State.BURN:
                self.setOutput(1, 1, 0)
            self.lastState = state

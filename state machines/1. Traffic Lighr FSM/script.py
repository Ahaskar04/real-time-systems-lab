from enum import Enum

class LightState(Enum):
    RED = 1
    GREEN = 2
    YELLOW = 3

# Transition Table
TRANSITIONS = {
    LightState.RED: LightState.GREEN,
    LightState.GREEN: LightState.YELLOW,
    LightState.YELLOW: LightState.RED,
}

class TrafficLight:
    def __init__(self):
        self.state = LightState.RED  # initial state

    def next(self):
        self.state = TRANSITIONS[self.state]
        return self.state

light = TrafficLight()

for _ in range(5):
    print(light.state)
    light.next()

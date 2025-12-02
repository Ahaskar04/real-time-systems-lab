from enum import Enum, auto

class LightState(Enum):
    RED = auto()
    GREEN = auto()
    YELLOW = auto()

class Event(Enum):
    TIMER_EXPIRED = auto()
    PED_BUTTON_PRESSED = auto()

class TrafficLightFSM:
    def __init__(self):
        self.state = LightState.RED
        self.pedestrian_waiting = False

    def handle_event(self, event: Event):
        if event == Event.PED_BUTTON_PRESSED:
            if self.state == LightState.GREEN:
                self.pedestrian_waiting = True
            return  # no immediate state change

        if event == Event.TIMER_EXPIRED:
            if self.state == LightState.RED:
                self.state = LightState.GREEN

            elif self.state == LightState.GREEN:
                self.state = LightState.YELLOW
                self.pedestrian_waiting = False  # reset after use

            elif self.state == LightState.YELLOW:
                self.state = LightState.RED

light = TrafficLightFSM()

print(light.state)
light.handle_event(Event.TIMER_EXPIRED)
print(light.state)

light.handle_event(Event.PED_BUTTON_PRESSED)
print("Ped waiting:", light.pedestrian_waiting)

light.handle_event(Event.TIMER_EXPIRED)
print(light.state)
print("Ped waiting:", light.pedestrian_waiting)

light.handle_event(Event.TIMER_EXPIRED)
print(light.state)

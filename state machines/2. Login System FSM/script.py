from enum import Enum, auto

class LoginState(Enum):
    LOGGED_OUT = auto()
    LOGGING_IN = auto()
    LOGGED_IN = auto()

class Event(Enum):
    START_LOGIN = auto()
    LOGIN_SUCCESS = auto()
    LOGIN_FAILURE = auto()
    LOGOUT = auto()

class LoginFSM:
    def __init__(self):
        self.state = LoginState.LOGGED_OUT

    def handle_event(self, event: Event) -> bool:
        # LOGGED_OUT
        if self.state == LoginState.LOGGED_OUT:
            if event == Event.START_LOGIN:
                self.state = LoginState.LOGGING_IN
                return True
            return False

        # LOGGING_IN
        if self.state == LoginState.LOGGING_IN:
            if event == Event.LOGIN_SUCCESS:
                self.state = LoginState.LOGGED_IN
                return True
            if event == Event.LOGIN_FAILURE:
                self.state = LoginState.LOGGED_OUT
                return True
            return False

        # LOGGED_IN
        if self.state == LoginState.LOGGED_IN:
            if event == Event.LOGOUT:
                self.state = LoginState.LOGGED_OUT
                return True
            return False

fsm = LoginFSM()

print(fsm.state)  # LOGGED_OUT

fsm.handle_event(Event.START_LOGIN)
print(fsm.state)  # LOGGING_IN

# External credential check happens here
password_correct = True

if password_correct:
    fsm.handle_event(Event.LOGIN_SUCCESS)
else:
    fsm.handle_event(Event.LOGIN_FAILURE)

print(fsm.state)  # LOGGED_IN

fsm.handle_event(Event.LOGOUT)
print(fsm.state)  # LOGGED_OUT

fsm = LoginFSM()

fsm.handle_event(Event.LOGIN_SUCCESS)  # False
fsm.handle_event(Event.LOGOUT)         # False

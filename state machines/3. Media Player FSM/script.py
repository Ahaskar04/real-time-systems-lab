from enum import Enum, auto


class PlayerState(Enum):
    STOPPED = auto()
    PLAYING = auto()
    PAUSED = auto()
    BUFFERING = auto()


class Event(Enum):
    CLICK_PLAY = auto()
    CLICK_PAUSE = auto()
    STOP = auto()
    BUFFER_EMPTY = auto()
    BUFFER_READY = auto()
    MEDIA_ENDED = auto()

class MediaPlayerFSM:
    def __init__(self):
        self.state = PlayerState.STOPPED

    def handle_event(self, event: Event) -> bool:
        if self.state == PlayerState.STOPPED:
            if event == Event.CLICK_PLAY:
                self.state = PlayerState.BUFFERING
                return True
            return False

        if self.state == PlayerState.BUFFERING:
            if event == Event.BUFFER_READY:
                self.state = PlayerState.PLAYING
                return True
            if event == Event.STOP:
                self.state = PlayerState.STOPPED
                return True
            return False

        if self.state == PlayerState.PLAYING:
            if event == Event.CLICK_PAUSE:
                self.state = PlayerState.PAUSED
                return True
            if event == Event.BUFFER_EMPTY:
                self.state = PlayerState.BUFFERING
                return True
            if event == Event.MEDIA_ENDED:
                self.state = PlayerState.STOPPED
                return True
            if event == Event.STOP:
                self.state = PlayerState.STOPPED
                return True
            return False

        if self.state == PlayerState.PAUSED:
            if event == Event.CLICK_PLAY:
                self.state = PlayerState.PLAYING
                return True
            if event == Event.BUFFER_EMPTY:
                self.state = PlayerState.BUFFERING
                return True
            if event == Event.STOP:
                self.state = PlayerState.STOPPED
                return True
            return False

player = MediaPlayerFSM()

print(player.state)  # STOPPED

player.handle_event(Event.CLICK_PLAY)
print(player.state)  # BUFFERING

player.handle_event(Event.BUFFER_READY)
print(player.state)  # PLAYING

player.handle_event(Event.CLICK_PAUSE)
print(player.state)  # PAUSED

player.handle_event(Event.CLICK_PLAY)
print(player.state)  # PLAYING

player.handle_event(Event.MEDIA_ENDED)
print(player.state)  # STOPPED

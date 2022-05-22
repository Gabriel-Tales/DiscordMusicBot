from enum import Enum, auto

class channelState(Enum):
    PLAY = auto()
    PLAYING = auto()
    PAUSE = auto()
    SKIP = auto()
    AFK = auto()
    DISCONNECTED = auto()
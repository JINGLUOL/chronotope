from dataclasses import dataclass


@dataclass
class SpriteStatus:
    IDLE = 'idle'
    FOLLOW = 'follow'
    CALL = 'call'
    CLICKED = 'clicked'
    pass

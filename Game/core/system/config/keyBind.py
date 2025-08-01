from curses import (
    KEY_UP   ,
    KEY_RIGHT,
    KEY_DOWN ,
    KEY_LEFT
)


class KeyBind:
    up    = KEY_UP
    right = KEY_RIGHT
    down  = KEY_DOWN
    left  = KEY_LEFT

    dungeonMap     = 9  # Tab
    debug          = 68 # Shift + D
    keyRecord      = 82 # Shift + R
    statusUIDesign = 83 # Shift + S
    cameraMove     = 67 # Shift + C
    openChat       = 10 # Enter

    volumeDown = 91 # [
    volumeUp   = 93 # ]
    mute       = 92 # \

    whistle    = 122 # Z
    playerMode = 120 # X

    slot1, slot2, slot3 = 49, 50, 51 # 1, 2, 3
    slot4, slot5, slot6 = 52, 53, 54 # 4, 5, 6

    itemInfo = 105 # I
    useItem  = 101 # E
    putItem  = 113 # Q

    pause = 32 # space

    SE1, SE2, SE3 = 33, 64, 35 # Shift + [1, 2, 3]
    SE4, SE5, SE6 = 36, 37, 94 # Shift + [4, 5, 6]
    SE7, SE8, SE9 = 38, 42, 40 # Shift + [7, 8, 9]

    SEUP, SEDOWN  = 45, 61 # -, =
from curses import KEY_UP, KEY_RIGHT, KEY_DOWN, KEY_LEFT


class KeyBind:
    up    = KEY_UP
    right = KEY_RIGHT
    down  = KEY_DOWN
    left  = KEY_LEFT

    dungeonMap     = 9 # Tab
    debug          = 68 # Shift + D
    keyRecord      = 82 # Shift + R
    statusUIDesign = 83 # Shift + S
    cameraMove     = 67 # Shift + C

    volumeDown = 91 # [
    volumeUp   = 93 # ]
    mute       = 92 # \

    whistle    = 122 # Shift + Z
    playerMode = 120 # Shift + M

    slot1, slot2, slot3 = 49, 50, 51 # 1, 2, 3
    slot4, slot5, slot6 = 52, 53, 54 # 4, 5, 6

    pause = 32 # space
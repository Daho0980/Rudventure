import curses


class KeyBind:
    up    = curses.KEY_UP
    right = curses.KEY_RIGHT
    down  = curses.KEY_DOWN
    left  = curses.KEY_LEFT

    dungeonMap     = 9
    debug          = 68
    keyRecord      = 82
    statusUIDesign = 83
    cameraMove     = 67

    volumeDown = 91
    volumeUp   = 93
    mute       = 92

    whistle    = 122
    playerMode = 120

    slot1, slot2, slot3 = 49, 50, 51
    slot4, slot5, slot6 = 52, 53, 54

    pause = 32
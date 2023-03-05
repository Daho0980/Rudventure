from Packages.lib      import stages, player
from Packages.lib.data import rooms, status

S1, s, r, p = stages, status, rooms, player.player
setGoal = 0

def quest(stage):
    global setGoal

    output = 0
    
    if stage == 0:
        if len(s.entities) == 0 and s.roomName == "field": s.room[0][2] = s.R
        if s.room[3][3] == s.p1:
            output = 1

    elif stage == 1:
        if len(s.entities) == 0:
            if s.room[20][11] == s.p1:
                output = 1

    elif stage == 2:
        btnPos1 = s.room[s.btnY][s.btnX]
        btnPos2 = s.room[s.btn1Y][s.btn1X]
        if btnPos1 == '☒' and btnPos2 == '☒':
            if btnPos1 in ['.', ' ']: btnPos1 = '✘'
            elif btnPos2 in ['.', ' ']: btnPos2 = '✘'
            if setGoal == 0:
                s.room[4][0] = s.goal
                setGoal += 1
            if s.room[4][0] == s.p1:
                output  = 1
                setGoal = 0

    elif stage == 3:
        if s.room[9][14] == s.p1:
            output = 1

    elif stage == 4:
        if len(s.entities) == 0:
            if setGoal == 0:
                setGoal += 1
                s.room[0][7] = s.goal
            if s.room[0][7] == s.p1:
                output = 1
                setGoal = 0


    return output


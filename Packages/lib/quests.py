from Packages.lib      import player, stages
from Packages.lib.data import rooms, status

S1, s, r, p = stages, status, rooms, player.player
isGoal = False

def trash(stage):
    global isGoal
    output = 0
    
    if stage == 0:
        if len(s.entities) == 0 and s.roomName == "field": s.room[0][2] = s.R
        if s.room[3][3] == s.p1 and s.roomName == "room_1": output = 1

    elif stage == 1:
        if len(s.entities) == 0 and s.room[20][11] == s.p1: output = 1

    elif stage == 2:
        btnPos1 = s.room[s.btnY][s.btnX]
        btnPos2 = s.room[s.btn1Y][s.btn1X]
        if btnPos1 in ['.', ' ']: btnPos1 = s.boxMark
        if btnPos2 in ['.', ' ']: btnPos2 = s.boxMark
        if btnPos1 == '☒' and btnPos2 == '☒' and isGoal == False:
            s.room[4][0] = s.goal
            isGoal = True
            
        if s.room[4][0] == s.p1: output = 1; isGoal = False

    elif stage == 3:
        if s.room[9][14] == s.p1: output = 1

    elif stage == 4:
        if len(s.entities) == 0 and isGoal == False:
            s.room[0][7] = s.goal
            isGoal = True
            
        if s.room[0][7] == s.p1 and isGoal == True: output = 1; isGoal = False

    return output


def quest():
    output = 0
    if s.Dungeon[s.Dy][s.Dx]['roomType'] == 4 and s.Dungeon[s.Dy][s.Dx]['room'][6][6] in [s.p1, s.p2]: output = 1
    return output

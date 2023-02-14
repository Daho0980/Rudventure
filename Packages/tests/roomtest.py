from modules import player, rooms, states, stages, quests
import playsound, os

p, r, s, q = player.player, rooms, states, quests.quest
s.y, s.x = 4, 3
s.hp = 1000000
s.room = r.field
s.stage = 2
stages.stages.stage(s.stage)

def moveInp():
    output = input("")

    return output

def fieldPrint():
        print(f"hp : {s.hp}/{s.Mhp} | def : {s.df}/{s.Mdf}\natk : {s.atk}\nhunger : {s.hunger}")
        for i in range(len(s.room)):
            print(' '.join(map(str, s.room[i])))
            i += 1

while True:
    while s.main > 0:
        q(s.stage)
        fieldPrint()
        move = moveInp()
        if move == 'w' or\
        move == 'a' or\
        move == 's' or\
        move == 'd':
            p.move(move, 1)
        elif move == 'H':
            p.Interaction('H')
        else:
            s.room[s.y][s.x] = '@'
        os.system('clear')
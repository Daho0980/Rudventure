import json

import uh as states
Vars = [name for name in dir(states) if not name.startswith('__')]
uselessVars = ['doorRooms', 'doors', 'p1', 'e', 'wall', 'R', 'item', 'goal', 'floor', 'fakeFloor', 'STOP', 'TFP', 'Rooms', 'room', 'r', 's', 'os', 'LOGO', 'colors']
for i in uselessVars: Vars.remove(i)
# print(Vars)
# for i in range(len(Vars)): print(f'{Vars[i]} : ' + str(eval(f'states.{Vars[i]}')))

def saveFile():
    file_path = './savefile.json'
    data = {}
    data['Data'] = []
    StatesData = {}
    for i in Vars:
        # data['states'].append({i : eval(f'states.{i}')})
        StatesData[i] = eval(f"states.{i}")
    data['Data'].append({"states" : StatesData})

    with open(file_path, "w") as outfile: json.dump(data, outfile, indent=4, ensure_ascii=False)

saveFile()
from Packages.modules import status
Vars = [name for name in dir(status) if not name.startswith('__')]
uselessVars = ['doorRooms', 'doors', 'p1', 'e', 'wall', 'R', 'item', 'goal', 'floor', 'fakeFloor', 'TFP', 'Rooms', 'room', 'r', 's', 'os', 'LOGO', 'colors', 'boss', 'Wanted', ]
for i in uselessVars: Vars.remove(i)
print(Vars)
for i in range(len(Vars)): print(f'{Vars[i]} : ' + str(eval(f'states.{Vars[i]}')))
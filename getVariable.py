from Packages.modules import states
Vars = [name for name in dir(states) if not name.startswith('__')]
uselessVars = ['doorRooms', 'doors', 'p1', 'e', 'wall', 'R', 'item', 'goal', 'floor', 'fakeFloor', 'STOP', 'TFP', 'Rooms', 'room', 'r', 's', 'os', 'LOGO', 'colors']
for i in uselessVars: Vars.remove(i)
print(Vars)
for i in range(len(Vars)): print(f'{Vars[i]} : ' + str(eval(f'states.{Vars[i]}')))
# import time
# import threading

# def func1():
#     global flag
#     flag = threading.Event()
#     while not flag.is_set():
#         for i in range(0,50):
#             time.sleep(0.2)
#     print("func1 die")

# def func2():
#     total=0
#     for i in range(0,30) :
#         total += i
#         time.sleep(0.5)
#         if total >= 55 :
#             print("func2 die")
#             return 1

# t1=threading.Thread(target=func1)
# t2=threading.Thread(target=func2)
# t1.daemon=True
# t2.daemon=True

# t1.start()
# t2.start()
# t2.join()
# flag.set()
# t1.join()

# print("exit") #input()

# if True:
#     print('a')
# elif False:
#     print('b')

# import playsound, threading, time

# sound = ''

# def soundPlay():
#     print('a')
#     if sound != '':
#         playsound.playsound(sound)

# def changeSound(text):
#     global sound

#     sound = f'sounds/{text}.wav'
#     time.sleep(0.001)
#     sound = ''

# asdf = threading.Thread(target=soundPlay, name='asdf')
# asdf.start()

# changeSound('defeat')
# changeSound('ClEar')
# # 특: 안됨

# from pynput import keyboard
# import time
# import os

# isActive = True
# asdf = True

# def key_press(key):
#     global asdf
#     if asdf == True:
#         print(key)
        

# def key_release(key):
#     # print(f'{key} release')
#     if key == keyboard.Key.esc:
#         global isActive
#         isActive = False
#         return False

# # with keyboard.Listener(on_press=key_press, on_release=key_release) as listener:
# #     listener.join()

# listener = keyboard.Listener(on_press=key_press,on_release=key_release)
# listener.start()

# print("실행중")
# for i in range(5):
#     if i == 3:
#         asdf = False
#     os.system('clear')
#     print('Program is running...')
#     time.sleep(1)
# print('bye')

# del listener


import os, subprocess

print(os.path.isdir('./main.py'))

a = 'b'
exec(f'{a} = [\'2\']')
print(b)

a = 'map_0'
exec(f'{a} = [\'2\']')
exec(f'{a}.append([])')
exec(f'{a}[{1}].append(\'4\')')
print(eval(a))

a = '1'
b = '2'
if int(a or b) > (0 or -1):
    print('fu')

for i in range(1, 7):
    print(i)

a = 1.23
print(f'{int(a)}\n')

# g = 0
# while True:
#     if g == 5:
#         continue
#     print(g)
#     g += 1

if ('a' or 'b' or 'c' or 'd') != int:
    print('a')

# a = ['a', 'b', 'c']
# print(a)
# a.remove(0)
# print(a)
a = []
b = 0
a.append(b)
print(a)
b+=1
a.append(b)
print(a)

minus = 0
for i in range(10):
    print(f'{i-minus}\n')
    if i-minus == 7:
        print('fu')
        minus += 1
        continue

a = {'a' : '1', 'b' : '2', 'c' : '3'}
print(list(a))

a = dict()
a['0'] = 'a'
print(a['0'])

y, x = 0, 2
room = 'fuck'
doorRooms = ['fuck', 'you', 'code']
doors = [[[0,2,5,3,'shit']], [[6,3,1,2,2]], [[5,10,5,0,3]]]

print(doorRooms.index)
nowRdoorsNum = doors[doorRooms.index(room)]
print(f'{y} {x} {room}')
for i in range(len(nowRdoorsNum)):
    if nowRdoorsNum[i][0] == y and nowRdoorsNum[i][1] == x:
        y = nowRdoorsNum[i][2]
        x = nowRdoorsNum[i][3]
        room = nowRdoorsNum[i][4]
        print(f'{y} {x} {room}')
        break

Vars = []
for name in dir():
    if not name.startswith('__'):
        Vars.append(name)
print(Vars)

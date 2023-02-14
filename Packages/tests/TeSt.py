

# 원하는 줄에 이상한 문구 저장
with open('modules/states.py', 'r') as f:
    data = f.readlines()
    for i in range(len(data)):
        if data[i].startswith('doorRooms') or data[i].startswith('doors'):
            data[i] = 'ㅇㅅㅇ\n'
            with open('modules/states.py', 'w') as a:
                a.writelines(data)
        else:
            print(data[i], end='')

with open('modules/states.py', 'a') as f:
    f.writelines('와 샌즈')
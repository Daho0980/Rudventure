from   Packages.globalFunctions import clear
import pip, sys

def install(package):
    if hasattr(pip, 'main'): pip.main(['install', package])
    else: pip._internal.main(['install', package])

downloadModuleList = []

modules = ['playsound', 'pynput']
for i in modules:
    try: exec(f'import {i}')
    except: downloadModuleList.append(i)

if len(downloadModuleList) > 0:
    print('게임 실행에 필요한 모듈을 받으려고 합니다. 확인 후 Enter키를 눌러주세요.\n받을 파일:')
    for i in downloadModuleList: print(f'    {i}')
    input('\n__확인')
    for i in downloadModuleList: install(i)
    clear()
    input('모듈 다운로드가 완료되었습니다. 게임을 껐다가 다시 켜주시길 바랍니다.\n\n__확인')
    sys.exit()
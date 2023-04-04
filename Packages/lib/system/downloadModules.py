"""
게임 구동 시 필요한 pip lib 다운로드 옵션
"""

import pip, sys
from   Packages.lib.system.globalFunc.graphic import clear
from   Packages.lib.system.globalFunc.system  import inp

def install(package:str):
    if hasattr(pip, 'main'): pip.main(['install', package])
    else                   : pip._internal.main(['install', package])
    clear()

downloadModuleList = []

clear()
modules = ['playsound', 'pynput']
for i in modules:
    try   : exec(f'import {i}')
    except: downloadModuleList.append(i)

if len(downloadModuleList) > 0:
    print('게임 실행에 필요한 라이브러리를 받으려고 합니다. 확인 후 Enter키를 눌러주세요.\n받을 라이브러리:')
    for i in downloadModuleList: print(f'    {i}')
    inp('\n__확인'); clear()

    for i in downloadModuleList: install(i)
    clear()
    inp('모든 라이브러리 다운로드가 완료되었습니다. 게임을 껐다가 다시 켜주시길 바랍니다.\n\n__확인'); clear()
    sys.exit()
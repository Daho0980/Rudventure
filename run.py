#!/usr/bin/env python3.13
import sys, os

from Assets.data import totalGameStatus as s


s.s             = '/'
pythonDirectory = "/Library/Frameworks/Python.framework/Versions/3.13/lib"

directory = os.path.dirname(os.path.realpath(__file__))
sys.path  = [
    directory,
    os.path.join(pythonDirectory, 'python313.zip'),
    os.path.join(pythonDirectory, 'python3.13'),
    os.path.join(pythonDirectory, 'python3.13', 'lib-dynload'),
    os.path.join(directory, 'lib', 'python3.13', 'site-packages')
]

if f"{s.pythonVersion.major}{s.pythonVersion.minor}{s.pythonVersion.micro}" != "3130":
    print(f"""이런! 파이썬 3.13.0이 설치되어 있지 않은 것 같습니다. || 현재 파이썬 버전 : {s.pythonVersion.major}.{s.pythonVersion.minor}.{s.pythonVersion.micro}
아래 링크를 눌러 파이썬을 다운로드해 주세요.
https://www.python.org/ftp/python/3.13.0/python-3.13.0-macos11.pkg
    """
    )
    exit(1)

from Game.core.system.dataLoader import makePath


s.TFP = str(os.path.abspath(''))+s.s

s.path['blockData'] = {k:makePath(*p)for k,p in s.path['blockData'].items()}
s.path['blockInfo'] = {k:makePath(*p)for k,p in s.path['blockInfo'].items()}

os.system("clear"if os.name=="posix"else"cls")
import Game.main
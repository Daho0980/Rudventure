#!/usr/bin/env python3.10
import sys, os
from   Assets.data import status as s

if os.name == 'posix':
    directory       = os.path.dirname(os.path.realpath(__file__))
    pythonDirectory = "/Library/Frameworks/Python.framework/Versions/3.10/lib"

    sys.path  = []
    sys.path.append(directory)
    sys.path.append(os.path.join(pythonDirectory, 'python310.zip'))
    sys.path.append(os.path.join(pythonDirectory, 'python3.10'))
    sys.path.append(os.path.join(pythonDirectory, 'python3.10', 'lib-dynload'))
    sys.path.append(os.path.join(directory, 'lib', 'python3.10', 'site-packages'))

pyV = sys.version_info

if f"{pyV.major}{pyV.minor}{pyV.micro}" != "31011":
    print("""이런! 파이썬 3.10.11이 설치되어 있지 않은 것 같습니다.
아래 링크를 눌러 파이썬 3.10.11을 다운로드해 주세요.

사이트 : https://www.python.org/downloads/release/python-31011/
                
MacOS  : https://www.python.org/ftp/python/3.10.11/python-3.10.11-macos11.pkg
                
Windows 32-bit : https://www.python.org/ftp/python/3.10.11/python-3.10.11.exe
Windows 64-bit : https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
    """
    )
    exit(1)

s.s   = {'posix':'/', 'nt':'\\'}[os.name]
s.TFP = str(os.path.abspath(''))+s.s

os.system("clear" if os.name == "posix" else "cls")
import Game.main
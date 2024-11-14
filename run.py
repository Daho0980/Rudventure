#!/usr/bin/env python3.10
import sys, os

from Assets.data import totalGameStatus as s


directory = os.path.dirname(os.path.realpath(__file__))

match os.name:
    case 'posix':
        s.s             = '/'
        pythonDirectory = "/Library/Frameworks/Python.framework/Versions/3.10/lib"

        sys.path = [
            directory,
            os.path.join(pythonDirectory, 'python310.zip'),
            os.path.join(pythonDirectory, 'python3.10'),
            os.path.join(pythonDirectory, 'python3.10', 'lib-dynload'),
            os.path.join(directory, 'lib', 'python3.10', 'site-packages')
        ]
    case 'nt':
        s.s             = '\\'
        pythonDirectory = "%APPDATA%\\Local\\Programs\\Python\\Python310"

        sys.path = [
            directory,
            os.path.join(pythonDirectory, 'python310.zip'),
            os.path.join(pythonDirectory, 'DLLs'),
            os.path.join(pythonDirectory, 'lib'),
            pythonDirectory,
            os.path.join(pythonDirectory, 'lib', 'site-packages')
        ]

pyV = sys.version_info

if f"{pyV.major}{pyV.minor}{pyV.micro}" != "31011":
    print(f"""이런! 파이썬 3.10.11이 설치되어 있지 않은 것 같습니다. || 현재 파이썬 버전 : {pyV.major}.{pyV.minor}.{pyV.micro}
아래 링크를 눌러 파이썬 3.10.11을 다운로드해 주세요.

사이트 : https://www.python.org/downloads/release/python-31011/

MacOS  : https://www.python.org/ftp/python/3.10.11/python-3.10.11-macos11.pkg

Windows 32-bit : https://www.python.org/ftp/python/3.10.11/python-3.10.11.exe
Windows 64-bit : https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
    """
    )
    exit(1)

s.TFP = str(os.path.abspath(''))+s.s

os.system("clear"if os.name=="posix"else"cls")
import Game.main
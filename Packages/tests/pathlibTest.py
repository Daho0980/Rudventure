from pathlib import Path
import os

s = ''
if os.name == "posix": s = '/'
else: s = '\\'

TFP = f"{Path.cwd()}{s}"

print("\n\n\n\n\n")
print(f"os getcwd : {os.getcwd()}")
print(f"현재 폴더 절대경로 : {Path.cwd()}")
print(f"파일 절대경로 :      {Path('pathlibTest.py').resolve()}")
# print(Path('C:\\Users\\hlee\\Desktop\\작업폴더\\main.py').name) output : C:\Users\hlee\Desktop\작업폴더\main.py
# print(Path('main.py').stem) 파일명
# print(Path('main.py').suffix) 확장자
import os
from   Packages.lib.data import status

s          = '/' if os.name == 'posix' else '\\'
status.TFP = str(os.path.abspath(f'Packages'))+s

os.system("clear" if os.name == "posix" else "cls")
exec(open(os.path.abspath(f'Packages{s}main.py'), encoding='utf8').read())
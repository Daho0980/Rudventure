import os, sys

s = ''
if os.name == "posix": s = '/'
else: s = '\\'

TFP = f'{os.getcwd()}{s}'
print(f'It called by {TFP}Packages{s}main.py')

try: exec(open(f'{TFP}Packages{s}main.py').read())
except:
    try: exec(open(f'Packages{s}main.py').read())
    except: sys.exit()
    else: sys.exit()
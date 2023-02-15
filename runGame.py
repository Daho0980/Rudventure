import sys, os
from pathlib import Path

s = ''
if os.name == "posix": s = '/'
else: s = '\\'

TFP = f"{Path.cwd()}{s}"
# Path(f'Packages{s}main.py').resolve()
print(f"It called by {Path('pathlibTest.py').resolve()}")

try: exec(open(f'{TFP}Packages{s}main.py').read())
except:
    try: exec(open(f'Packages{s}main.py').read())
    except: sys.exit()
    else: sys.exit()
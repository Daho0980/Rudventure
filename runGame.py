import os
from pathlib import Path

s = ''
if os.name == "posix": s = '/'
else: s = '\\'

TFP = f"{Path.cwd()}{s}"
print(f"It called by {Path('runGame.py').resolve()}")

exec(open(Path(f'Packages{s}main.py').resolve(), encoding='utf8').read())
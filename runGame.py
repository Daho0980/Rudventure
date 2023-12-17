import os
from   Assets.data import status as s

s.s = {'posix':'/', 'nt':'\\'}[os.name]
s.TFP = str(os.path.abspath(''))+s.s

os.system("clear" if os.name == "posix" else "cls")
import Game.main
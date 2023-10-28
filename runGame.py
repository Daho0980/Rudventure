import os
from   Packages.lib.data import status as s

s.s = {'posix':'/', 'nt':'\\'}[os.name]
s.TFP = str(os.path.abspath(f'Packages'))+s.s

os.system("clear" if os.name == "posix" else "cls")
import Packages.main
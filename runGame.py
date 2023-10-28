import os
from   Packages.lib.data import status as s

s.TFP = str(os.path.abspath(f'Packages'))+{'posix':'/', 'nt':'\\'}[os.name]
'/' if os.name == 'posix' else '\\'
os.system("clear" if os.name == "posix" else "cls")
import Packages.main
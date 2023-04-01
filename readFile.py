import os
from   Packages.lib.system.Secret.rudConverter      import converter
from   Packages.lib.data import status as s

s.s = "/"

try:
    a = open(f"{os.getcwd()}/Packages/saveFiles/someData.json", 'r')

    encoded = converter.encode(a.readlines())
    print(encoded)
    with open(f"{os.getcwd()}/Packages/saveFiles/someData.json", 'w') as outFile:
        for line in encoded: outFile.write(f"{line}\n")
    converter.changeExtention("someData", beforeExt=".json", afterExt=".rud")
except:
    with open(f"{os.getcwd()}/Packages/saveFiles/someData.rud", 'r') as returnFile:
        lines = returnFile.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i][:-1]
    
    with open(f"{os.getcwd()}/Packages/saveFiles/someData.rud", 'w') as outFile:
        for line in converter.decode(lines): outFile.write(line)
    converter.changeExtention("someData")


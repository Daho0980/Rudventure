from os.path import isfile, isdir
from re      import compile
from json    import dump, load

from .                 import status  as s
from Assets.data.color import cColors as cc


_extEditor = compile(r'\.[^.]+$')

def classifier(name:str) -> tuple:
    filePath = f"{s.pathText}/{name}"

    return (
        "file"
            if isfile(filePath)
        else "folder"
            if isdir(filePath)
        else "unknown",
        _extEditor.sub('', name)
    )

def documentation(data:tuple[tuple[str, str], bool]) -> str:
    if data[0][0] in s.skipType:
        return (
            f"{cc['bg']['F']}{s.itemIcon[data[0][0]]} | {data[0][1]}{cc['end']}"
                if data[1]
            else f"{s.itemIcon[data[0][0]]} | {data[0][1]}"
        )
    
    fileAccess, newFile = s.lockData[data[0][1]]

    if data[1]:
        prefixColor = cc['bg']['F']
        newMark     = f" {cc['bg']['R']}!" if newFile and fileAccess else ""

    else:
        prefixColor = "" if fileAccess else cc['fg']['G1']
        newMark     = f" {cc['fg']['R']}!" if newFile and fileAccess else ""
    
    return f"{prefixColor}* | {data[0][1]}{newMark}{cc['end']if prefixColor or newMark else''}"

def loadLock() -> None:
    s.lockData = load(open(f"{s.pathText}/_lock.json", 'r', encoding="UTF-8"))

def saveLock() -> None:
    dump(
        s.lockData,
        open(f"{s.pathText}/_lock.json", 'w', encoding="UTF-8"),
        ensure_ascii=False,
        indent      =4
    )

    s.lockData.clear()
import json, os

from Assets.data import status as s


def reset() -> None:
    with open(f"{s.TFP}config{s.s}data.json", 'w') as data:
        json.dump(
            {
                "statusDesign"      : 1,
                "debugConsole"      : False,
                "showDungeonMap"    : 0,
                "frameRate"         : -1,
                "volume"            : 50,
                "autoTerminalSize"  : False,
                "checkTerminalSize" : True
            },
            data,
            indent=4
        )

def load() -> None:
    with open(f"{s.TFP}config{s.s}data.json", 'r') as f:
        data = json.load(f)

        s.statusDesign      = data["statusDesign"]
        s.debugConsole      = data["debugConsole"]
        s.showDungeonMap    = data["showDungeonMap"]
        s.frameRate         = data["frameRate"]
        s.frame             = 1/data["frameRate"]      if data["frameRate"] else 0
        s.volume            = data["volume"]
        s.autoTerminalSize  = data["autoTerminalSize"]
        s.checkTerminalSize = data["checkTerminalSize"]

def save() -> None:
    with open(f"{s.TFP}config{s.s}data.json", 'w') as data:

        json.dump(
            {
                "statusDesign"      : s.statusDesign,
                "debugConsole"      : s.debugConsole,
                "showDungeonMap"    : s.showDungeonMap,
                "frameRate"         : s.frameRate,
                "volume"            : s.volume,
                "autoTerminalSize"  : s.autoTerminalSize,
                "checkTerminalSize" : s.checkTerminalSize,
                "mtsY"              : s.sss['minimum'][0],
                "mtsX"              : s.sss['minimum'][1]
            },
            data,
            indent=4,
            ensure_ascii=True
        )

if not os.path.exists(f"{s.TFP}config{s.s}data.json"): reset()
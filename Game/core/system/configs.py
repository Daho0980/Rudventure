import json, os

from Assets.data import status as s


def reset() -> None:
    with open(f"{s.TFP}config{s.s}data.json", 'w') as data:
        json.dump(
            {
                "system": {
                    "statusDesign"  : 1,
                    "debugConsole"   : False,
                    "showDungeonMap": 0,
                    "frameRate"     : -1,
                    "volume"        : 50
                }
            },
            data,
            indent=4
        )

def load() -> None:
    with open(f"{s.TFP}config{s.s}data.json", 'r') as f:
        data = json.load(f)

        s.statusDesign   = data["system"]["statusDesign"]
        s.debugConsole    = data["system"]["debugConsole"]
        s.showDungeonMap = data["system"]["showDungeonMap"]
        s.frameRate      = data["system"]["frameRate"]
        s.frame          = 1/data["system"]["frameRate"] if data["system"]["frameRate"] else 0
        s.volume         = data["system"]["volume"]

def save() -> None:
    with open(f"{s.TFP}config{s.s}data.json", 'w') as data:

        json.dump(
            {
                "system": {
                    "statusDesign"  : s.statusDesign,
                    "debugConsole"   : s.debugConsole,
                    "showDungeonMap": s.showDungeonMap,
                    "frameRate"     : s.frameRate,
                    "volume"        : s.volume
                }
            },
            data,
            indent=4,
            ensure_ascii=True
        )

if not os.path.exists(f"{s.TFP}config{s.s}data.json"): reset()
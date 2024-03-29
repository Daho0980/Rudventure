import json, os

from Assets.data import status as s


def reset() -> None:
    with open(f"{s.TFP}config{s.s}data.json", 'w') as data:
        json.dump(
            {
                "system": {
                    "statusDesign"  : 1,
                    "debugScreen"   : False,
                    "showDungeonMap": 0,
                    "frameRate"     : -1
                }
            },
            data,
            indent=4
        )

def load() -> None:
    with open(f"{s.TFP}config{s.s}data.json", 'r') as f:
        data = json.load(f)

        s.statusDesign   = data["system"]["statusDesign"]
        s.debugScreen    = data["system"]["debugScreen"]
        s.showDungeonMap = data["system"]["showDungeonMap"]
        s.frameRate      = data["system"]["frameRate"]
        s.frame          = 1/data["system"]["frameRate"] if data["system"]["frameRate"] else 0

def save() -> None:
    with open(f"{s.TFP}config{s.s}data.json", 'w') as data:

        json.dump(
            {
                "system": {
                    "statusDesign"  : s.statusDesign,
                    "debugScreen"   : s.debugScreen,
                    "showDungeonMap": s.showDungeonMap,
                    "frameRate"     : s.frameRate
                }
            },
            data,
            indent=4,
            ensure_ascii=True
        )

if not os.path.exists(f"{s.TFP}config{s.s}data.json"): reset()
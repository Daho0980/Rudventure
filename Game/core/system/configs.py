import json, os
from   Assets.data import status as s

if not os.path.exists(f"{s.TFP}config{s.s}data.json"):
    with open(f"{s.TFP}config{s.s}data.json", 'w') as data:
        json.dump(
            {
                "allSound" : True,
                "sound"    : {
                    "hostileMob"  : True,
                    "friendlyMob" : True,
                    "interaction" : True,
                    "system"      : True,
                    "player"      : True
                }
            },
            data,
            indent=4
        )

def load():
    with open(f"{s.TFP}config{s.s}data.json", 'r') as f:
        data = json.load(f)

        s.allSound = data["allSound"]
        for uh in ["hostileMob", "friendlyMob", "interaction", "system", "player"]:
            s.sound[uh] = data["sound"][uh]

def save():
    with open(f"{s.TFP}config{s.s}data.json", 'w') as data:
        json.dump(
            {
                "allSound" : s.allSound,
                "sound"    : {
                    "hostileMob"  : s.sound["hostileMob"],
                    "friendlyMob" : s.sound["friendlyMob"],
                    "interaction" : s.sound["interaction"],
                    "system"      : s.sound["system"],
                    "player"      : s.sound["player"]
                }
            },
            data,
            indent=4,
            ensure_ascii=False
        )
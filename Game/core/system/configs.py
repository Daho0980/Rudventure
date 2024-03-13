import json, os

from Assets.data import status as s
from Assets.data import color as c

if not os.path.exists(f"{s.TFP}config{s.s}data.json"):
    with open(f"{s.TFP}config{s.s}data.json", 'w') as data:
        json.dump(
            {
                "color": {
                    "fg" : {
                        "B" :   "\033[;38;5;0m",
                        "M" :   "\033[;38;5;1m",
                        "G" :   "\033[;38;5;2m",
                        "O" :   "\033[;38;5;3m",
                        "N" :   "\033[;38;5;4m",
                        "P" :   "\033[;38;5;5m",
                        "T" :   "\033[;38;5;6m",
                        "S" :   "\033[;38;5;7m",
                        "G1" :  "\033[;38;5;8m",
                        "R" :   "\033[;38;5;9m",
                        "L" :  "\033[;38;5;10m",
                        "Y" :  "\033[;38;5;11m",
                        "B1" : "\033[;38;5;12m",
                        "F" :  "\033[;38;5;13m",
                        "A" :  "\033[;38;5;14m",
                        "W" :  "\033[;38;5;15m"
                    },
                    "bg" : {
                        "B" :   "\033[;48;5;0m",
                        "M" :   "\033[;48;5;1m",
                        "G" :   "\033[;48;5;2m",
                        "O" :   "\033[;48;5;3m",
                        "N" :   "\033[;48;5;4m",
                        "P" :   "\033[;48;5;5m",
                        "T" :   "\033[;48;5;6m",
                        "S" :   "\033[;48;5;7m",
                        "G1" :  "\033[;48;5;8m",
                        "R" :   "\033[;48;5;9m",
                        "L" :  "\033[;48;5;10m",
                        "Y" :  "\033[;48;5;11m",
                        "B1" : "\033[;48;5;12m",
                        "F" :  "\033[;48;5;13m",
                        "A" :  "\033[;48;5;14m",
                        "W" :  "\033[;48;5;15m",
                    },
                    "end" : "\033[0m"
                },
                "colorList": {
                    "fg": [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True],
                    "bg": [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
                }
            },
            data,
            indent=4
        )

def load():
    with open(f"{s.TFP}config{s.s}data.json", 'r') as f:
        data = json.load(f)

        c.cColors = data["color"]
        for fg, bg, i in zip(data["colorList"]["fg"], data["colorList"]["bg"], range(16)):
            c.colorList[0][i][0], c.colorList[1][i][0] = fg, bg


def save():
    with open(f"{s.TFP}config{s.s}data.json", 'w') as data:

        json.dump(
            {
                "color" : c.cColors,
                "colorList": {
                    "fg": list(map(lambda arr: arr[0], c.colorList[0])),
                    "bg": list(map(lambda arr: arr[0], c.colorList[1]))  
                }
            },
            data,
            indent=4,
            ensure_ascii=True
        )

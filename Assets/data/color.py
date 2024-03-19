cColors:dict = {
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
}

colorList:list =  [
    [
        [True, "\033[;38;5;0m", "Black",    "B"],
        [True, "\033[;38;5;1m", "Maroon",   "M"],
        [True, "\033[;38;5;2m", "Green",    "G"],
        [True, "\033[;38;5;3m", "Olive",    "O"],
        [True, "\033[;38;5;4m", "Navy",     "N"],
        [True, "\033[;38;5;5m", "Purple",   "P"],
        [True, "\033[;38;5;6m", "Teal",     "T"],
        [True, "\033[;38;5;7m", "Silver",   "S"],
        [True, "\033[;38;5;8m", "Grey",    "G1"],
        [True, "\033[;38;5;9m", "Red",      "R"],
        [True, "\033[;38;5;10m", "Lime",    "L"],
        [True, "\033[;38;5;11m", "Yellow",  "Y"],
        [True, "\033[;38;5;12m", "Blue",   "B1"],
        [True, "\033[;38;5;13m", "Fuchisa", "F"],
        [True, "\033[;38;5;14m", "Aqua",    "A"],
        [True, "\033[;38;5;15m", "White",   "W"]
    ],
    [
        [True, "\033[;48;5;0m", "Black",    "B"],
        [True, "\033[;48;5;1m", "Maroon",   "M"],
        [True, "\033[;48;5;2m", "Green",    "G"],
        [True, "\033[;48;5;3m", "Olive",    "O"],
        [True, "\033[;48;5;4m", "Navy",     "N"],
        [True, "\033[;48;5;5m", "Purple",   "P"],
        [True, "\033[;48;5;6m", "Teal",     "T"],
        [True, "\033[;48;5;7m", "Silver",   "S"],
        [True, "\033[;48;5;8m", "Grey",    "G1"],
        [True, "\033[;48;5;9m", "Red",      "R"],
        [True, "\033[;48;5;10m", "Lime",    "L"],
        [True, "\033[;48;5;11m", "Yellow",  "Y"],
        [True, "\033[;48;5;12m", "Blue",   "B1"],
        [True, "\033[;48;5;13m", "Fuchisa", "F"],
        [True, "\033[;48;5;14m", "Aqua",    "A"],
        [True, "\033[;48;5;15m", "White",   "W"]
    ]
]

customColor=lambda R,G,B,T=1:f"\033[{[0,38,48][T]};2;{R};{G};{B}m"
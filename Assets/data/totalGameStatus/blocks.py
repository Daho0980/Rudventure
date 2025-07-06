bids:dict[str,str] = {
    "void" : '  ',
    "floor" :  ' ',
    "wall" :  '██',
    "door" :  '. ',
    "orbBox" :  'É',
    "exit" :  'F',

    "squishy0" :  'O',
    "squishy1" :  'o',

    "hpOrbS" : 'o',
    "dfOrbS" : 'q',
    "atkOrbS" : 'v',
    "hgOrbS" : 'o',
    "csOrbS" : 'ø',

    "hpOrbB" : 'O',
    "dfOrbB" : 'Q',
    "atkOrbB" : 'V',
    "hgOrbB" : 'O',
    "csOrbB" : 'Ø',

    "clayModel" : '☷',
    "deadClayModel" : '☷',

    "flower" : '*',
    "petal" : '.',
    "item" : '?',
    "corpse" : 'X',
    "blood" : '░',

    "normalStatue" : 'Y',
    "cursedStatue" : 'Y',

    "aorta" : 'H',
    "venaCava" : 'U',

    "ashChip" : ';'
}

bloodIcon:dict[int,str] = {
    5 : "██",
    4 : "█▓",
    3 : "▓▒",
    2 : "▒░",
    1 : "░",
}

orbData = {
    "S" : {
        "hp"  : 1,
        "df"  : 1,
        "atk" : 1,
        "hg"  : 100,
        "cs"  : 1
    },
    "B" : {
        "hp"  : 3,
        "df"  : 2,
        "atk" : 2,
        "hg"  : 250,
        "cs"  : 5
    }
}
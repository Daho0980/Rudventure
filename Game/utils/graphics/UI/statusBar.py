from Assets.data.color import cColors as cc


BAR_TYPES:dict[str, tuple[str, str]] = {
    "Normal"   : ("[", "]"),
    "Cursed"   : ("<", ">"),
    "Exaltation" : ("{", "}"),
    "Curved"   : ("(", ")")
}

def get(status        :int          ,
        color         :str          ,
        statusName    :str =""      ,
        maxStatus     :int =0       ,
        emptyCellColor:str =""      ,
        barType       :str ="Normal",
        frontTag      :str =""      ,
        backTag       :str =""      ,
        showComma     :bool=True    ,
        usePercentage :bool=False   , 
        showEmptyCell :bool=True     ) -> str:
    emptyCellColor = emptyCellColor or cc['fg']['G1']
    maxStatus      = maxStatus      or status

    Display     = []
    displayCell = 0

    Display.append(f"{
            f'{statusName} '
                if len(statusName)>0
            else ''
        } {frontTag} {cc['fg']['G1']}{BAR_TYPES[barType][0]}{color}"
    )

    if usePercentage:
        status, maxStatus = round((status/maxStatus)*10), 10

    displayCell = maxStatus if status>maxStatus else status

    Display.append(f"{
        '|'*displayCell
        +emptyCellColor
        +'|'*(
            (maxStatus-displayCell)
                if showEmptyCell
            else 0
        )
        }{cc['fg']['G1']}{BAR_TYPES[barType][1]}{cc['end']}"
    )

    if (status-maxStatus) > 0: Display.append(f" {color}+{status-maxStatus}{cc['end']}")

    Display.append(f"{',' if len(backTag)>0 and showComma else ''} {backTag}")

    return ''.join(Display)
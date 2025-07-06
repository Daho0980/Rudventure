LVL_CHAR = ("░", "▒", "▓", "█")

def get(level:int, width:int=10, charType:tuple=()) -> str:
    charType = charType or LVL_CHAR
    OLV, TLV = divmod(level, int(100/width))
    return ((charType[3]*OLV)+(charType[round(TLV*(3/width))])+(charType[0]*(width-OLV)))[:width]
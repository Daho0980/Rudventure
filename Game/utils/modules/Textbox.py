from re        import compile
from itertools import chain

from Assets.data.color        import cColors   as cc
from Game.utils.graphics      import escapeAnsi
from Game.utils.RSExt.libtext import measure, cut


BOX_OVER  = 0b10
BOX_UNDER = 0b1

boxLineData:dict[str,dict[int,tuple[str, str]]] = {
    "normal" : {0:("┌", "┐"), 1:("└", "┘"), 2:("├", "┤"), 3:("─", "│")},
    "double" : {0:("╔", "╗"), 1:("╚", "╝"), 2:("╠", "╣"), 3:("═", "║")},
    "bold"   : {0:("┏", "┓"), 1:("┗", "┛"), 2:("┣", "┫"), 3:("━", "┃")},
    
    "cornerDouble" : {0:("╔", "╗"), 1:("╚", "╝"), 2:("╠", "╣"), 3:("─", "┃")},
}

_TBMacroRegex = compile(r"TextBox\.([^_]+)_")

def _getMacroCMD(text:str) -> str|None:
    if (data:=_TBMacroRegex.search(text)): return data.group(1)

def _getTextInsertedLine(pos      :str           ,
                         text     :str           ,
                         corner   :tuple[str,str],
                         bar      :str           ,
                         padWidth :int           ,
                         isCovered:bool          ,
                         end      :str           ,
                         color    :str            ) -> str:
    match pos:
        case "middle":
            halfLine = bar*int(padWidth/2)
            output   = f"{halfLine}{text}{''if isCovered else color}{halfLine}{bar if padWidth&1 else ''}"
    
        case "left":  output = f"{text}{bar*padWidth}"
        case "right": output = f"{bar*padWidth}{text}"

    return f"{color}{corner[0]}{output}{corner[1]}{end}"


def TextBox(Inp:str,
            
            maxLine    :int            =100      ,
            extendWidth:int            =0        ,
            inDistance :tuple[int, int]=(0, 0b00),
            outDistance:tuple[int, int]=(0, 0b00),

            Type       :str            ="left"            ,
            fillChar   :str            =" "               ,
            LineType   :str            ="normal"          ,
            sideText   :str            =""                ,
            coverColor :str            =""                ,
            sideTextPos:tuple[str,str] =("over", "middle"),

            AMLS         :bool=False,
            safeBox      :bool=True ,
            textSplit    :bool=True ,
            endLineBreak :bool=False,
            overEllipsis :bool=False,
            returnSizeyx :bool=False,
            coverSideText:bool=False,
            height       :int =0                           ) -> str:
    """
    Inp **(str)**:
        글상자의 내용.
        줄바꿈하려면 `\\n`을 사용해야 함

    Type **(str["left", "middle", "right"])**:
        글상자 내용의 위치 설정.
        기본값 : `"left"`

    maxLine **(int)**:
        최대 박스 길이 설정.
        `AMLS`를 사용하는 경우 그대로 두는 것이 좋음.
        기본값 : `100`

    fillChar **(char)**:
        박스 안을 채울 캐릭터.
        기본값 : `" "`

    inDistance **(tuple[int>=0, 0b{2}])**:
        박스 내부 상하 공백 크기 설정.
        기본값 : `(0, 0b00)`

    outDistance **(tuple[int>=0, 0b{2}])**:
        박스 외부 상하 공백 크기 설정.
        기본값 : `(0, 0b00)`

    extendWidth **(int>=0)**:
        텍스트 양 옆 거리 설정.
        기본값 : `0`

    AMLS **(bool)**:
        가장 긴 텍스트의 길이에 대한 박스 너비 설정 여부.
        이미 maxLine을 설정했다면 신경쓰지 않는 게 좋음.
        기본값 : `False`

    endLineBreak **(bool)**:
        개행 문자 여부.
        기본값 : `False`

    returnSizeyx **(bool)**:
        박스 크기 추가 반환 여부.
        기본값 : `False`

    LineType **(str["normal", "double", "bold", "cornerDouble"])**:
        글상자 테두리 종류 설정.
        기본값 : `"normal"`

    safeBox **(bool)**:
        무조건적 박스 반환 여부.
        기본값 : `True`

    sideText **(str)**:
        글상자 선 사이에 들어갈 텍스트.
        기본값 : `""`

    sideTextPos **(tuple[str("over", "under"), str("left", "middle", "right")])**:
        `sideText`가 들어갈 위치.
        기본값 : `("over", "middle")`

    coverSideText **(bool)**:
        `sideText` 양 옆을 선이 감쌀지에 대한 여부.
        기본값 : `False`

    coverColor **(str)**:
        박스와 내부 텍스트를 채울 색.
        텍스트에 색이 들어가 있다면 다시 채워지지 않음.
        기본값 : `" "`

    textSplit **(bool)**:
        문장이 maxLine 초과 시 분할 여부.
        `AMLS`를 사용하는 경우 그대로 두는 것이 좋음.
        기본값 : `True` 
    """
    if not len(Inp):
        if not safeBox: return ""
        Inp = "..."

    Display = []

    outline     = []
    upperInline = []
    lowerInline = []

    endLine  = '\n'      if endLineBreak else ''
    end      = cc['end'] if coverColor   else ''

    boxLine = boxLineData[LineType]
    boxBar  = boxLine[3][0]
    boxSide = f"{coverColor}{boxLine[3][1]}{end}"

    if AMLS:
        maxLine = max(map(
            lambda l: measure(escapeAnsi(l)),
            chain((txtLines:=Inp.split('\n')), [sideText])
        ))
    
    else:
        txtLines = cut(Inp, maxLine, textSplit, overEllipsis, height)

    boxWidth  = maxLine+(extendWidth*(1+(Type=="middle")))
    emptyLine = f"{boxSide}{fillChar*boxWidth}{boxSide}"

    if sideText:
        if coverSideText:
            sideText = f"{boxLine[2][1]}{sideText}{coverColor}{boxLine[2][0]}"

        sidePadWidth = boxWidth-measure(escapeAnsi(sideText))

    if outDistance[1]&0b11: outline = ['']*outDistance[0]

    extra = (len(txtLines)-Inp.count('\n')-1)
    match inDistance[1]:
        case 0b10: upperInline = [emptyLine]*(inDistance[0]-extra)
        case 0b01: lowerInline = [emptyLine]*(inDistance[0]-extra)
        case 0b11:
            upperInline = [emptyLine]*(inDistance[0]-(extra//2))
            lowerInline = [emptyLine]*(inDistance[0]-(extra//2)+(extra&1))

    del extra

    if outDistance[1]&BOX_OVER: Display.extend(outline)
    Display.append(
        _getTextInsertedLine(
            sideTextPos[1],
            sideText,
            boxLine[0],
            boxBar,
            sidePadWidth,
            coverSideText,
            end,
            coverColor
        )\
            if  sideText\
            and sideTextPos[0]=="over"\
        else f"{coverColor}{boxLine[0][0]}{boxBar*boxWidth}{boxLine[0][1]}{end}"
    )
    if inDistance[1]&BOX_OVER: Display.extend(upperInline)

    for txtLine in txtLines:
        space    = measure(escapeAnsi(txtLine))
        padWidth = maxLine-space

        if txtLine.startswith("TextBox."):
            match _getMacroCMD(txtLine):
                case "Line":
                    Display.append(
                        f"{coverColor}{boxLine[2][0]}{boxBar*boxWidth}{boxLine[2][1]}{end}"
                    )

                case "Middle":
                    halfSpace = (padWidth//2)+7

                    Display.append(
                        f"{boxSide}{fillChar*(halfSpace+extendWidth)}{
                            txtLine.lstrip('TextBox.Middle_')
                        }{fillChar*(halfSpace+extendWidth+(padWidth&1)+1)
                        }{boxSide}"
                    )

                case "Left":
                    Display.append(
                        f"{boxSide}{txtLine.lstrip('TextBox.Left_')}{
                            fillChar*(padWidth+13+extendWidth)\
                        }{boxSide}"
                    )

                case "Right":
                    Display.append(
                        f"{boxSide}{
                            fillChar*(padWidth+14+extendWidth)
                        }{txtLine.lstrip('TextBox.Right_')}{boxSide}"
                    )

        else:
            match Type:
                case "middle":
                    halfSpace = padWidth//2

                    Display.append(
                        f"{boxSide}{fillChar*(halfSpace+extendWidth)}{
                            txtLine
                        }{fillChar*(halfSpace+extendWidth+(padWidth&1))
                        }{boxSide}"
                    )
                    
                case "left":
                    Display.append(
                        f"{boxSide}{txtLine}{
                            fillChar*(padWidth+extendWidth)
                        }{boxSide}"
                    )

                case "right":
                    Display.append(
                        f"{boxSide}{
                            fillChar*(padWidth+extendWidth)
                        }{txtLine}{boxSide}"
                    )

    if inDistance[1]&BOX_UNDER:
        Display.extend(lowerInline)
    Display.append(
        _getTextInsertedLine(
            sideTextPos[1],
            sideText,
            boxLine[1],
            boxBar,
            sidePadWidth,
            coverSideText,
            end,
            coverColor
        )\
            if  sideText\
            and sideTextPos[0]=="under"\
        else f"{coverColor}{boxLine[1][0]}{boxBar*boxWidth}{boxLine[1][1]}{end}{endLine}"
    )
    if outDistance[1]&BOX_UNDER: Display.extend(outline)

    if returnSizeyx: return len(Display)-(outDistance[0]*2), maxLine+2, '\n'.join(Display) # type: ignore
    else:            return '\n'.join(Display)


# How to use:
# print(
#     TextBox("기본 박스(100칸)"),
#     TextBox("왼쪽\n(Type=left)", Type="left"),
#     TextBox("중간\n(Type=middle)", Type="middle"),
#     TextBox("오른쪽\n(Type=right)", Type='right'),
#     TextBox("최대 길이 자동 설정\n아래에 짧은 줄이 있든\n\n존나 긴 줄이 있든 알아서 정해줌\n\n(현재: Type=middle, AMLS=True)", Type="middle", AMLS=True),
#     TextBox("글상자 안/밖 거리 설정도 가능\n\n(inDistance=5, outDistance=3, AMLS=True, Type=middle)", inDistance=5, outDistance=3, AMLS=True, Type="middle"),
#     TextBox("일반"),
#     TextBox("볼드 (LineType=bold)", LineType="bold"),
#     TextBox("더블 (LineType=double)", LineType='double'),
#     sep="\n\n"
# )
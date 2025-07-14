from Assets.data       import totalGameStatus as s
from Assets.data.color import cColors         as cc


def get() -> str:
    step   = [(0, 3), (1, 4), (2, 5)]
    output = []

    for cellColumn in step:
        lines = []
        for cellIndex in cellColumn:
            if cellIndex < len(s.inventory['cells']):
                
                boxColor = cc['fg']['Y']\
                        if s.inventory['pointer']==cellIndex\
                    else cc['fg']['G1']\
                        if s.inventory['cells'][cellIndex]['disabled']\
                    else ''
                
                cell = (
                    f"{boxColor}┏━{cellIndex+1}━┓{cc['end']}",

                    f"{boxColor}┃{cc['end']} {
                        ' '\
                            if not s.inventory['cells'][cellIndex]['item']\
                        else s.inventory['cells'][cellIndex]['item']['icon']
                    } {boxColor}┃{cc['end']}",

                    f"{boxColor}┗━━━┛{cc['end']}"
                )
                lines.extend(cell)

        if len(lines) > 3:
            lines = [
                f"{lines[0]}{lines[3]}",
                f"{lines[1]}{lines[4]}",
                f"{lines[2]}{lines[5]}"
            ]

        if lines: output.append(f"{lines[0]}\n{lines[1]}\n{lines[2]}\n")
        
    return "".join(output)
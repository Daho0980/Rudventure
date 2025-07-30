from Assets.data                      import totalGameStatus as s
from Assets.data.color                import cColors         as cc
from functions.grammar                import pstpos          as pp
from Game.core.system.io.logger       import addLog
from Game.core.system.data.dataLoader import elm


def weightCalculate(func):
    def wrapper(*args) -> str:
        func(*args)

        if args[3] == '∞': return "treadOn"
        
        if sum(map(
            lambda cell: cell['item']['status']['weight'] if cell['item'] else 0,
            s.inventory['cells']
        )) > args[3]:
            name = elm(
                    f"Assets/data/info/item/{args[2]}.json",
                    f"{args[1]}.name", 'string'
                )
            addLog(
                f"{cc['fg']['R']}'{name}'{pp(name,'sub',True)} 파괴되었습니다!{cc['end']}", # type: ignore
                colorKey='R'
            )

            return "destroyed"
        
        return "treadOn"

    return wrapper
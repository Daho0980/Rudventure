from Assets.data                      import totalGameStatus as s
from Assets.data.color                import cColors         as cc
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
            addLog(
                f"{cc['fg']['R']}'{elm(
                    f"Assets/data/info/item/{args[2]}.json",
                    f"{args[1]}.name", 'string'
                )}'이 파괴되었습니다!{cc['end']}",
                colorKey='R'
            )

            return "destroyed"
        
        return "treadOn"

    return wrapper
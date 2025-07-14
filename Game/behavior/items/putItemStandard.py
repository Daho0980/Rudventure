from Game.core.system.io.logger import addLog
from Game.tools                 import inventory


def putItem(func):
    def wrapper(*args) -> None:
        match inventory.put():
            case "itemPopFailure":
                addLog("아이템을 버리는 데 실패했습니다.")

            case "allowedBlockNotFound":
                addLog("이 주변에서는 아이템을 버릴 수 없습니다.")

        func(*args)

    return wrapper
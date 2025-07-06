from Assets.data import totalGameStatus as s


def interactSound() -> tuple:
    return ("player", "interaction", "repo", "nom")\
        if s.playerIdentity == 'repo'\
    else ("player", "getItem")
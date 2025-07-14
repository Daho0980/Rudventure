from Assets.data       import totalGameStatus as s
from Assets.data.color import cColors         as cc


def main(func):
    def wrapper(*args):
        func(*args)

        _tool()
        _weapon()
        _consumable()

    return wrapper

def _tool():
    s.iids['tool']['ásotus'] = f"{cc['fg']['G1']}Ⴔ{cc['end']}"

def _weapon():
    s.iids['weapon']['animus']       = f"{cc['fg']['B1']}⇀{cc['end']}"
    s.iids['weapon']['anima']        = f"{cc['fg']['B1']}⇁{cc['end']}"
    s.iids['weapon']['animusAnima']  = f"{cc['fg']['B1']}⇋{cc['end']}"

def _consumable(): pass
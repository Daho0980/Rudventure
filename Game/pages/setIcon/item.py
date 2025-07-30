from Assets.data       import totalGameStatus as s
from Assets.data.color import cColors         as cc


def main(func):
    def wrapper(*args):
        func(*args)

        s.originMark = {
            "badal" : f"{cc['fg']['N']}신국 바달{cc['end']}",
            "qantalotia" : f"{cc['fg']['A']}콴탈로티아{cc['end']}",
            "ethlem" : f"{cc['fg']['P']}에틀렘{cc['end']}",
            "vamulhen" : f"{cc['fg']['M']}바뮬헨{cc['end']}",
            "samarGavim" : f"{cc['fg']['W']}사마르 가빔{cc['end']}",
            "nimDraha" : f"{cc['fg']['L']}님 드라하{cc['end']}",
            "senixn" : f"{cc['fg']['B1']}세닉션{cc['end']}"
        }

    return wrapper
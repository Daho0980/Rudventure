import time

from Assets.data             import lockers as l
from Game.utils.system.sound import play


def TTS(text, voice:str="glagatrof", delay=0.07):
    if l.useSound:
        for char in text:
            if char not in [' ', '.', ',']:
                play("player", "voice", voice)
            time.sleep(delay)
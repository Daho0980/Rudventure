import re
import time

from Assets.data             import lockers as l
from Game.utils.system.sound import play


def TTS(
        text,
        voicePath:tuple=("player", "voice", "glagatrof"),
        delay:float|int=0.07
        ) -> None:
    if l.useSound:
        text = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]').sub('',text)
        
        for char in text:
            if char not in [' ', '.', ',']:
                play(*voicePath)
            time.sleep(delay)
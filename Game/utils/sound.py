"""
Global Functions 중 Sound 옵션

    ``play`` : 사운드가 중첩될 수 있게 만들어주는 함수
"""

import threading
import playsound
from   Assets.data import status as s

def play(File:str, raw:bool=False):
    """
    사운드가 중첩될 수 있게 만들어주는 함수\n\n

        `File`     : 사운드의 이름, 이름을 정확하게 하지 않으면 지랄발광을 할 수 있음, 무조건 기입해야 함, 또한 raw == True일 시 파일 위치 작성 가능\n
        `raw`      : 사운드 파일 위치를 직접 입력할지에 대한 여부, 기본적으로 `False`로 설정되어 있음
    """
    if s.sound:
        threading.Thread(
            target=lambda: playsound.playsound(
                f"{s.TFP}Assets{s.s}sounds{s.s}{File}.wav" if raw == False else File
                ),
            name  ="sound",
            daemon=True
            ).start()
"""
Global Functions 중 Sound 옵션

    ``play`` : 사운드가 중첩될 수 있게 만들어주는 함수
"""

import threading
import playsound
from   Assets.data import status as s

def play(File:str, kind:str='system'):
    """
    사운드가 중첩될 수 있게 만들어주는 함수\n\n

        `File`     : 사운드의 이름, 이름을 정확하게 하지 않으면 지랄발광을 할 수 있음, 무조건 기입해야 함\n
        `kind`     : 사운드의 종류, 설정에 맞게 실행되거나 실행되지 않을 수 있음, 기본적으로 `system`으로 설정되어 있음
                     종류는 아래와 같음:
                        hostileMob\n
                        friendlyMob\n
                        interaction\n
                        system\n
                        player
    """
    if s.allSound and s.sound[kind] and File:
        threading.Thread(
            target=lambda: playsound.playsound(
                f"{s.TFP}Assets{s.s}sounds{s.s}{File}.wav"
                ),
            name  ="sound",
            daemon=True
            ).start()
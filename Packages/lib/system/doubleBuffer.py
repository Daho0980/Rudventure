"""
더블 버퍼링을 적용한 출력 모듈

    ``DoubleBuffer``(class) : 더블 버퍼링에 필요한 모든 함수가 들어간 클래스

    사용 방법:
        var = `DoubleBuffer()`로 객체 생성\n
        `var.write(str(text))`로 문자열 저장\n
        `var.render()`로 저장된 버퍼 출력 후 버퍼 위치 변경\n
"""
import os, sys

class DoubleBuffer:
    """
    ``__init__`` : 더블 버퍼링에 필요한 매개변수들을 설정함
            `self.buffer`(list),
            `self.current`(int)
            가 있음\n
    ``write``    : self.buffer[self.current]에 위치한 문자열에 문자열 저장
    ``render``   : 준비된 텍스트를 sys 모듈을 활용해 clear 후 flush함
    """
    def __init__(self):
        """
        `self`(self) : 알빠노
        """
        self.buffer  = ['', '']
        self.current = 0
        self.clear_screen()

    def clear_screen(self):
        """
        `self`(self) : 알빠노
        """
        os.system("clear" if os.name == "posix" else "cls")

    def write(self, text:str):
        """
        `self`(self) : 알빠노
        `text`(str) : 버퍼에 저장할 문자열
        """
        self.buffer[self.current] += text

    def render(self):
        """
        `self`(self) : 알빠노
        """
        self.clear_screen()
        sys.stdout.write(self.buffer[self.current])
        sys.stdout.flush()
        self.buffer[self.current] = ''
        self.current              = 1 - self.current

# ex)
# if __name__ == '__main__':
#     double_buffer = DoubleBuffer()
#     while True:
#         double_buffer.write("""
# hp : 2/10 | def : 0/5
# hunger : 71% | atk : 2

#      5 [||||||||||] 6
# ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■
# ■ . . . . . . . . . . . ■
# ■ . . . . . . . . . . . ■
# ■ . . . . . . . . . . . ■
# ■ . . . . . . . . . . . ■
# ■ . . . . . . @ . . . . ▤
# ■ . . . . . . . . . . . ▤
# ■ . . . . . . . . . . . ▤
# ■ . . . . . . . . . . . ■
# ■ . . . . . . . . . . . ■
# ■ . . . . . . . . . . . ■
# ■ . . . . . . . . . . . ■
# ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■ ■
# 고통의_편린_5이(가) 죽었습니다!
# 고통의_편린_3이(가) 2만큼의 피해를 입었습니다! (체력 : 2)
# 고통의_편린_3이(가) 죽었습니다!
#         """)
#         double_buffer.render()
#         time.sleep(1/60)
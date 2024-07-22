from Assets.data.color       import cColors           as cc
from Assets.data             import status as s
from Game.core.system        import configs
from Game.utils.modules      import cSelector, Textbox
from Game.utils.system       import cinp
from Game.utils.system.sound import play


clc = cSelector

def main(stdscr) -> None:
    if s.checkTerminalSize:
        y, x = stdscr.getmaxyx()
        isy, isx = False if y < s.sss['minimum'][0] else True, False if x < s.sss['minimum'][1] else True

        if (isy+isx)<=1:
            match clc.main(
                Textbox.TextBox(
                    f"{cc['fg']['R']}무, 무슨?!{cc['end']}",
                    Type        ="middle",
                    AMLS        =True,
                    inDistance  =1,
                    addWidth    =5,
                    coverColor  =cc['fg']['R'],
                    endLineBreak=True
                )+f"""
현재 터미널의 {['높이', ''][isy]}{[['와 너비가', '가'],['너비가', '']][isy][isx]}
게임 최소 기준에 부합하지 않습니다.

다음부터 자동으로 재조정하시겠습니까?""",
                ["네", "아니오", "두 번 다신 내 화면에 나오지 마쇼.\n  이건 내 마지막 경고요."],
                [1,0,255,10],
                '@'):
                case 1:
                    s.autoTerminalSize = True
                    configs.save()
                    stdscr.clear()
                    cinp(
                        stdscr,
                        f"설정이 완료되었습니다. 자동 터미널 크기\n설정 변경은 이후 설정에서 하실 수 있습니다.\n확인 시 메인 메뉴로 넘어갑니다.\n\n{cc['fg']['L']}@ [Enter]키를 눌러 확인{cc['end']}"
                    )
                    play("system", "selector", "select")
                case 3:
                    s.checkTerminalSize = False
                    configs.save()
                    stdscr.clear()
                    cinp(
                        stdscr,
                        f"확인되었습니다. 터미널 크기 확인은\n이후 설정에서 하실 수 있습니다.\n확인 시 메인 메뉴로 넘어갑니다.\n\n{cc['fg']['L']}@ [Enter]키를 눌러 확인{cc['end']}"
                    )
                    play("system", "selector", "select")
            stdscr.clear(); stdscr.refresh()
            return
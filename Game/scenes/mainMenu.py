import curses

from   Assets.data                  import status     as s
from   Game.core.system             import configs
from   Game.scenes                  import checkColor
from   Game.utils.modules           import cSelector  as clc
from   Game.utils.sound             import play


def main(stdscr) -> None:
    configs.load()
    checkColor.main(stdscr)
    play("smash")
    while 1:
        mainMenu:int = clc.main(
            s.LOGO,
            {
                "나락 입장" : "건투를 빕니다.",
                "설정..."   : "게임에 관련된 설정을 합니다.",
                "조작법"    : "드... 드리겠습니다!!",
                "게임 종료" : "게임을 종료합니다."
            },
            [1,0,255,10],
            '@'
        )

        if mainMenu == 1: break

        elif mainMenu == 2:
            play("smash")
            while 1:
                mainSettings = clc.main(
                    "<< 설정 >>",
                    {
                        "소리" : "소리와 관련된 설정을 합니다.",
                        ""     : "",
                        "완료" : ""
                    },
                    [1,0,255,10],
                    '@'
                )
                match mainSettings:
                    case 1:
                        play("smash")
                        while 1:
                            soundSettings = clc.main(
                                "<< 소리 >>",
                                [
                                    f"모든 소리 : {s.allSound}",
                                    "",
                                    f"적대적인 몹 : {s.sound['hostileMob']}",
                                    f"친화적인 몹 : {s.sound['friendlyMob']}",
                                    f"상호작용    : {s.sound['interaction']}",
                                    f"시스템      : {s.sound['system']}",
                                    f"플레이어    : {s.sound['player']}",
                                    "",
                                    "완료"
                                ],
                                [1,0,255,10],
                                '@'
                            )
                            match soundSettings:
                                case 1: s.allSound = False if s.allSound else True
                                case 2: s.sound['hostileMob']  = False if s.sound['hostileMob']  else True
                                case 3: s.sound['friendlyMob'] = False if s.sound['friendlyMob'] else True
                                case 4: s.sound['interaction'] = False if s.sound['interaction'] else True
                                case 5: s.sound['system']      = False if s.sound['system']      else True
                                case 6: s.sound['player']      = False if s.sound['player']      else True
                                case 7: break
                            
                            configs.save()
                    case 2: break
            
        elif mainMenu == 3:
            clc.main("제작중", ["화긴"], [1,0,255,10], '@')

        elif mainMenu == 4:
            s.main = 0
            curses.endwin()
            exit(1)
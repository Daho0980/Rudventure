from datetime import datetime

from Assets.data.color import cColors as cc

from Assets.data import (
    totalGameStatus as s,
    comments        as c
)


s.playerColor      = ["\033[;38;5;32m", "CU"]
s.ids[300]         = f"{s.playerColor[0]}◑{cc['end']}"
s.playerVoice      = "upload"
s.playerDamageIcon = ['◐ ']

s.statusFormula = {
    "evasion"           : "s.evasionRate+(90-s.evasionRate)*((s.Mhp-s.hp)/s.Mhp)",
    "curseBloodSucking" : "s.hp -= 1"
}

s.RPL = [
"""if not s.stage and not s.isLoadfromBody and s.name.lower() in ["업로드", "upload"]:
    entity.addAnimal(
        200, 10, 1, 3, 6,
        name     ="구름이",
        color    =[cc['fg']['W'],'W'],
        friendly =True,
        MCBF     =True,
        SICR     =True,
        extraData={"loyalty":10}      )
if s.isLoadfromBody:
    entity.loadEntities()"""
]

c.lowHp = [
    "나 곧 뒤질듯 ㅋㅋ.",
    "한쪽 귀가 안들리는데?",
    "어지럽고 토할 것 같군. 아주 좋아.",
    "우우... 대가리 아푸...",
    "점점 숨쉬기가 힘든wwww.",
    "아니 이게 맞아?",
    "하하, 난 병신이야.",
    "오, 머리가 울리는 것이 매우 좃같군.",
    "아.",
    "아오 ㅋㅋ.",
    "플레이리스트를 조금 바꿀까.",
    "힝.",
]

c.treasureRoom = {
    0 : [
        "ㅋㅋ 실화냐.",
        "? 1개?",
        "아니!!!!!!!!",
        "기대도 안했다.",
        "이거 버그 아님?",
    ],
    1 : [
        "오.",
        "아니 이거 말고!!",
        "음;",
        "진짜 애매하네.",
        "적당히 기쁘네.",
    ],
    2 : [
        "우횻wwwwwwww.",
        "이거지 ㅋㅋㅋㅋㅋㅋㅋㅋ.",
        "와캬퍄헉쭉농 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ.",
        "이걸로 앨범 사야겠다 ㅋㅋ.",
        "와 ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ.",
    ]
}

c.defeat = {
    "HL" : [
        f"보고 피하면 쉬움 ㅋㅋ. -업로드 (2008 ~ {datetime.today().year})",
        "망겜.",
        "이게 죽어?",
        "아, 시원한 음료가 매우 마시고 싶군.",
        "아니!!!!!",
        "으악.",
    ],
    "HUL" : [
        "아유 배고파라.",
        "오 닭발 먹고싶다.",
        "오 곱창 먹고싶다.",
        "오 햄버거 먹고싶다.",
        "오 치킨 먹고싶다.",
        "타우린이 풍부한 얼짱쭈꾸미와 함께하는\n24시간 연속방송 들어간다.",
        "밥 사먹을 돈이 없네 ㅋㅋ.",
    ],
    "CO" : [
        "오, 나 좀 간지나는 듯.",
        "귀가 양쪽 다 안들리는데?",
        "시야가 왜 이렇게 흐릿하냐?",
        "속이 안좋아.",
        "이익...",
        "으으음...",
        "뭔가 쇠맛이 나는데?",
    ]
}

c.victory = {
    0 : [
        "ㅋㅋ 이걸 사네.",
        "어케 살음?",
        "졸려.",
        "나 한쪽 눈이 잘 안움직이는데?",
    ],
    1 : [
        "좀 별론데?",
        "이상한 냄새 나.",
        "이거 언제 끝나요?",
        "눈에 뭐 들어갔어.",
        "아이고 허리야.",
    ],
    2 : [
        "아직도 안끝났어?",
        "오늘따라 기분이 상쾌하군.",
        "히히.",
        "이거 괜찮네.",
        "와!",
    ],
    3 : [
        f"{cc['fg']['W']}♪Eve - {s.playerColor[0]}Dramaturgy♪{cc['end']}",
        f"{cc['fg']['W']}♪Eve - {s.playerColor[0]}Inochi no tabekata♪{cc['end']}",
        f"{cc['fg']['W']}♪Eve - {s.playerColor[0]}Raison d'etre♪{cc['end']}",
        f"{cc['fg']['W']}♪DAZBEE - {s.playerColor[0]}Sugarcoat♪{cc['end']}",
        f"{cc['fg']['W']}♪DAZBEE - {s.playerColor[0]}Bambi♪{cc['end']}",
        f"{cc['fg']['W']}♪DAZBEE - {s.playerColor[0]}Lovestruck♪{cc['end']}",
    ]
}

c.TIOTA = [
    "으, 끈적해.",
    "이이.",
    "뭐임? ㅋㅋ.",
    "으악 ㅋㅋ.",
    "아잇.",
]

c.collide = {
    "animal" : {
        "cat" : [
            "왜~?",
            "흐흥~",
            "아유 이뻐라~",
            "나 지금 조금 바쁜데...",
            "헤헹.",
        ],
        "catAttack" : [
            "앗.",
            "읏.",
            "핫.",
            "씁.",
            "왜 그래~",
        ]
    },
    "monster" : {

    }
}

c.clayModelAnswer = [
    "오 개꿀.",
    "묘하게 생겼네.",
    "오예.",
    "이건 걔도 좋아하겠네.",
    "으음.",
    "선물 좋구만.",
]

c.start = [
    "좋은 아침.",
    "매우 엄청나게 졸리군.",
    "내 이어폰 어디갔지?",
    "시야가 묘하네.",
    "한 30분만 깔끔하게 자고싶은데.",
    "여기 이상한 냄새나."
]

c.startWithCowardmode = [
    "응!",
    "그래!",
    "에라이.",
]

c.loadsaveStart = [
    "또 여기야?",
    "또?",
    "눈 아파.",
    "좀 닥쳐봐. 손톱 다 뽑아서 루브르 박물관에 전시하기 전에.",
]

c.monologue = {
    "HL" : [
        "시야가 흐릿한데...",
        "...",
        "아직 안되는데...",
        "...할 말이 있었는데.",
        "버틸만 한 것 같기도.",
    ],
    "HUL" : [
        "배고픈 건 익숙해.",
        "탄내가 심하네.",
        "물만 있으면 버틸만 할텐데.",
        "(콜록)",
        "집밥 안 먹은지 몇 년은 됐네.",
    ],
    "CO" : [
        "목이 따가워.",
        "그년은 죽여버렸어야 했는데.",
        "...보고싶다.",
        "기억이 묘하게 선명해졌는데.",
        "토할 것 같아.",
    ],
    "ELS" : [
        "흠~ 흐흠~",
        "음~",
        "...보고싶어라.",
        "후...",
        "인생 참.",
    ],
}

c.enterinBattle = {
    0 : [
        "덤벼.",
        "...고작?",
        "뭐, 이정도면...",
        "하아.",
        "익숙해.",
    ],
    5 : [
        "약하니까 뭉치는거지.",
        "이러면 나야 편하지.",
        "난 일대일이 특기인데.",
        "뭐, 안맞으면 돼.",
        "시간은 많아.",
    ]
}
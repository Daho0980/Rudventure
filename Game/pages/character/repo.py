from random import choice

from Assets.data.color import cColors as cc

from Assets.data import (
    totalGameStatus as s,
    percentage      as per,
    comments        as c
)


s.playerIdentity   = "repo"
s.playerColor      = ["\033[;38;5;92m", "CR"]
s.eids['player1']  = f"{s.playerColor[0]}ᓩ{cc['end']}"
s.playerVoice      = "repo"
s.playerDamageIcon = list(map(lambda c: f"{chr(c)} ", range(5124, 5184)))
                        
per.treasureComment = 100
per.monologue       = {
    "min" : 150,
    "max" : 450
}

foods = [
    "치킨 타코",
    "칠리 콘 카르네",
    "디트로이트 피자",
    "샐러드",
    "해바라기 씨앗",
    "밀웜",
    "총탄",
]

s.statusFormula = {
    "evasion"           : "s.evasionRate",
    "curseBloodSucking" : """
if s.hp == 1: s.Mhp += 1
else:         s.hp  -= 1
"""
}

c.lowHp = [
    "나 죽는다!! 죽는다고!!!",
    "으아악!!! 아퍼!!!",
    "끼에엑!!!",
    "이럴땐 소수를.... 소수를... 2..3....5...7..",
    "후우...후우.....",
    "Ph’nglui mglw’nafh Cthulhu R’lyeh wgah’nagl fhtagn...",
    "이이이이익!!! 이이이이이익!!!!",
    [
        "끄악!",
        "...나 살아있는 건 맞지?"
    ],
    "깃털 손질할 시간이네....",
    "깃털이 다 망가졌어...",
    "난 삼계탕이 되기 싫어...",
    "  ,ㄴ`  ",
]

c.treasureRoom = {
    0 : [
        "이런 날도 있는 거지...",
        "뭣.",
        "엥? 내 눈이 박살난 건가?",
        "기대했는데...",
        "쓰읍... 이건 좀...",
    ],
    1 : [
        "오...",
        "뭐...",
        "허어...",
        " ' ⊃' ",
        "적당하네...",
    ],
    2 : [
        "  ^ ⊃^ ",
        "많다 많아!",
        "오늘... 내 생일인가?",
        "오예!",
        "이히힛... 다 내꺼야!",
        "어라, 신기루? 이거 진짜야?",
    ]
}

c.defeat = {
    "HL" : [
        "너무해...",
        "...",
        "죽기 전에 한 마디만 할게... 이거 너무 아퍼...",
        "아... 영접하여 영광입니다 그 분이시여...",
        "우으... 뜌땨...",
        "우하하하하하핳",
    ],
    "HUL" : [
        f"어우... {choice(foods)} 좀 먹고 올 걸..."
    ],
    "CO" : [
        "아아...",
        "오... 기분 좋아...",
        "흐흫...",
        "따뜻해...",
        "휴......",
        "신선해요...",
        "우흣...",
        "끼우웅...",
    ]
}

c.victory = {
    0 : [
        "휴... 새고기 신세는 간신히 피했어.",
        "이긴 게 이긴 게 아니야..",
        "이러다간 내가 요리가 되어버린다고 제발...",
        "스튜 먹고 싶다..",
        "죽겠어요...",
    ],
    1 : [
        "또?",
        "그만 했으면 좋을텐데...",
        "지금 좀 아픈데... 쉬었다 요리하자...",
        "얼마나 더 해야..",
        "끝은 절대 끝은 절대 끝은 절대 끝은 절대...",
        "배고파...",
    ],
    2 : [
        "다음은 무슨 식재료가 있을까?",
        "좋은 향기...",
        "이번엔 무슨 요리를 할까?",
        "달콤한 피...",
        "혀가 짭짤해.",
        "눈은 좀 비렸어.",
    ],
    3 : [
        "이 정도면 즐거운 요리였어",
        "배부르다!",
        "더... 아니, 다 내놔!",
        "좋았어!",
        "이 층은 순종적인 식재료가 많았어!",
    ]
}

c.TIOTA = [
    "오, 전복 내장맛이네.",
    "이거... 모아서 요리 할 수 있나?",
    "하하 내 깃털은 방수야! ...부러졌지만 말이지.",
    "기분 나빠.",
    "깃털이 또 부러진 것 같아...",
]

c.collide = {
    "animal" : {
        "cat" : [
            "으아? 고...고양이?! 무서워...",
            "... 그쪽은 저를 잡아먹지 않으시나요?",
            "이런! 나는 아직 살 날이 많은데... 뭐요? 안 죽인다고요? 으음... 믿는 수밖에는...",
            "으악! 앗! 혀 깨물었어!",
            "(후덜덜덜덜)",
        ],
        "catAttack" : [
            "으앗! 제발 목숨만은!",
            "으악 제발",
            "제가 이렇게 싹싹 빌게요... 잡아먹지만 말아주세요...",
            "으악! 나 죽어!!! 죽는단 말이야!!!",
            "으악! 내 깃털!!",
        ]
    },
    "monster" : {

    }
}

c.clayModelAnswer = [
    "...나락에서 편히 잠드시길.",
    "...고마워요. 나락에서 편히 잠드시길.",
    "...애도를 표합니다. 나락에서 편히 잠드시길.",
    "......선물은 감사합니다. 나락에서 편히 잠드시길.",
    "하아... 나락에서 편히 잠드시길.",
]

c.start = [
    "내가 안 먹어본 식재료... 이곳에는 분명 있을 거야.",
    "올 블루라고 들어본 적 있어?",
    "분명 불빛 한 점 없는데 눈앞이 잘 보여... 왜일까?",
    "으으... 떨어지면서 깃털이 또 부러진 것 같아.",
    "이곳에서는 날지 못하는 거 같아... 공기가 없는 걸까?",
]

c.startWithCowardmode = [
    "칫, 그렇게 까지 말 안해도 안다고요!",
    "기분 나쁘게...",
    "쯧...",
    "시끄러워요. 전 더 많은 식재료를 탐구하는 것만이 최우선적인 목표라고요.",
    "제가 뭘하든 무슨 상관인가요, 미지의 목소리씨.",
    "그 부리를 함부로 놀리지 마시죠. 아, 부리가 없으신가?",
    "... 나중에 직접 보게 된다면 그 부리에 직접 붉은 사슴뿔버섯 유칼립투스 쌈밥을 먹여드리죠...",
    "어디 계신지만 알려주신다면 그 부리를 직접 뭉게버리러 갈 거예요...",
]

c.loadsaveStart = [
    "응애...",
    "나 자신을 요리하면 어떻게 되는 거지?",
    "이곳은 어떤 곳이길래 내 육체가 보존되는 걸까...",
]

c.monologue = {
    "HL" : [
        "아픈 건 싫은데...",
        "이러다 망가진 깃털의 수가 멀쩡한 깃털의 수보다 많아질 거 같아!",
        "후...힘든데....",
        "좀... 쉴까? 온몸에서 멀쩡한 곳이 적어...",
        [
            "온 몸에서 식은땀이 흘러...",
            "아, 기분 탓이었네. 내가 땀샘이 있을 리 만무하잖아?"
        ],
        "배고프진 않지만... 내장이 파열된 거 같아...",
        "으음... 나만 알고 있는 레시피를 적은 유언장을 사용할 날이 곧 올 거 같아.",
        "으윽...뼈가 쑤시네...",
        "조금만 더 맞으면 요리도 못하게 생겼어...",
    ],
    "HUL" : [
        "평소보다 배고파!!!",
        "으어... 그아악 나에게 밥을! 밥을 달란 말이야!!! 밥이 필요해... 밥이...",
        [
            "너무 배고파 이 던전 벽이라도 씹어 먹고 싶어...",
            "이 던전 벽은 원래 맛있어 보였으니까 맛있게 뜯어먹어도 되겠지?",
            "단단한지는 상관없어 아소투스가 나에게 벽을 요리해 줄 거야...",
            "벽을... 요리... 벽..."
        ],
        [
            "제대로 된 식량을 아소투스가 요리해 줬으면 하는데, 아소투스가 요리할 식재료가 필요해...",
            "당장이라도 다음 식재료를 찾자."
        ],
        [
            "으어....................",
            "배고...파..죽....는...다........."
        ],
        [
            "당장 떠오르는 요리 레시피만 하더라도 158개의 요리 레시피가 떠오르고, 내가 완벽히 기억하는 요리 레시피는 총합 384862개야.",
            "그런데 이런 레시피들을 지금 당장 활용할 수 없어? 왜 나는... 요리할 수 없어?",
            "왜 나는 고통받아?",
            "왜 나만?",
            "왜?",
            "왜?"
        ],
        [
            "세상이 너무 불공평한 거 같아. 나는 음식을 먹을 수 없다고?",
            "나는 왜 음식을 먹을 수 없는거야?",
            "왜 바닥이 흙이 아닌거야? 진흙 쿠키라도 소화 가능해서 좋은데...?"
        ],
        [
            "지금 당장 초콜릿이 있었다면 나는 당장 초콜릿을 조리해서 먹었을 거야.",
            "어째서인지 내 몸이 초콜릿만을 분해하지 못하고 독성을 보이지만...",
            "그래도, 그 독성 가득한 초콜릿을 나는 원해..."
        ],
        "파이...... 파스타... 스테이크... 만두... 찜... 국... 스튜... 수프...",
        [
            "흐윽...우흐으...흐으으악으흑크흑...",
            "우..우는 거 아니야... 젠장... 히윽..."
        ],
    ],
    "CO" : [
        "뭔가 익숙한 것들이 몸을 조여오는걸?",
        "아마 저주가 나를 구원해 주는 것만 같아... 이대로라면 곧....",
        "몸이 찌뿌둥한데... 스트레칭이나 좀 해야겠어.",
        "흫... 기분 좋아....",
        "흐으... 흐흐....",
        "아소... 흫....",
        "후... 흐흐....",
        "...",
        "좋아... 좋아... 좋아... 좋아해요....",
    ],
    "ELS" : [
        "아... 배고프다.",
        "아소투스? ...아직이야.",
        "아소투스는 도대체 왜 나와 동행한 거야? 말하기 싫다고? 그래...",
        "서늘한 게 냉장고가 필요 없을 거 같아... 물론 식재료에 저주만 묻지 않는다면 말이야.",
        "난 고양이가 무서워...",
        "이곳은 어떻게 빠져나갈까... 뭐 상관없나?",
        "이곳의 시간은 참 이상한 거 같아. 어떨 땐 뒤로 어떨땐 옆으로도 흘러.",
        [
            "그는 말했다. \"사람들 사이에 있더라도 외롭기는 마찬가지야.\"",
            "나는 그것에 답했다. \"나는 근처에 기댈 사람은 커녕 사람 자체가 없는걸?\"",
            "... 젠장."
        ],
        [
            "아... 돌이라도 끓여먹고 싶은 하루야.",
            "근데 맛있으려나? 회색맛이 나겠지?"
        ],
        [
            "나도 가끔은 조리해 먹기 귀찮을 때가 있어.",
            "그럴 때에는 조리를 안하고 생으로 먹지.",
            "음... 이 잿가루는 깊은 맛을 내면서도 씁쓸하고 매콤한 게 맛있는데?"
        ],
        "아직도 시간이 이만큼 밖에 흐르지 않았다고? 아, 시간이 멈춰있었구나!",
        "헝그리 정신은 가끔 필요하지... 근데 나는 이미 배고픈걸?? 더 굶으면 아마 굶어 죽고 말 거야...",
    ],
}

c.enterinBattle = {
    0 : [
        "쓰읍... 식재료가 적어...",
        "한 끼 정도는 겨우 나오겠어.",
        "너무 적어...",
        "후우... 아소투스도 굶주려 하고 있어.",
        "... 이걸 누구 코에 붙이라고..."
    ],
    5 : [
        "뭐라고 아소투스? 전부 요리하자고? 저걸...?",
        [
            "오늘은 잔칫상을 만들 수 있겠네.",
            "오늘이 아니라 어제인가?"
        ],
        "... 아 군침 돌았어.",
        "우와! 식재료들이 이렇게 많다고? 이거 너무 좋다! 내가 먹을 음식이 더 많이 늘어나겠어!",
        "이 식재료들이 빨리 썩지 않게 보존처리만 한다면...",
    ]
}

c.curseDecrease = {
    "middleOver" : [
        "흐유... 그래도 아직까지는...",
        "안돼! 저주가 씻겨나가고 있잖아!!",
        "만지지마 만지지마 만지지마 만지지마 만지지마 만지지마 만지지마 만지지마 만지지마",
        "괜찮아! 더 만지지만 않으면 된다구.",
        "기분 나빠...",
        "그냥 만지지 않아도 되지 않을까...",
        "아직 기분 좋아. 그러니까, 더 건들지는 말아줘...",
        "너, 그거 하지마.",
        "건들지마!!!!!",
        "하, 젠장.",
        "나, 너무 기분 나쁜데..?",
        "우으으... 나에게서 저주를 뺏어가지마...",
        "저주... 적어졌어...",
        "안돼! 으아아악!!"
    ],
    "middleUnder" : [
        "이건... 뭐 하는 짓이야?",
        "...",
        "후...",
        "아..."
    ],
    "Under" : [
        [
            "오호... 저주가 아주 조금 씻겨나간 기분이야.",
            "기분이 딱히 좋지는 않네."
        ],
        "뭐... 아주 살짝 저주가 씻겨내려간 느낌이야.",
        "뭐지... 이 기분은...",
        "신상... 딱히 기분 좋은 울림은 아니네."
    ]
}

c.getOrb = {
    "hp" : {
        "hpLow" : {
            "S" : [
                "...이게 끝이야?",
                "부족해...",
                "아직...",
                "아 제발 조금 더 주면 안 되는거야?",
                "더 없어? 정말? 진짜로?",
                "나 아직 아프다고...",
	            "이거 약간 피맛이 나는거 같은데... 아, 내 입에서 나는 피구나.",
	            "...나 살아있는건 맞지? 방금 전에 눈 앞이 캄캄해졌었다구..."
            ],
            "B" : [
                "...그나마.",
                "하아... 고비는 넘긴거 같은데?",
                "아직 많이 부족하지만, 이 정도라면 몇 발자국 정도야 나아갈 수 있겠지...",
                "히야앗... 정말 죽는 줄 알았다구!",
                "우왓! 위험했어...",
	            "어우 심장이..."
            ]
        },
        "notHpLow" : {
            "S" : [
                "음! 달콤하고 맛있어!",
                "음! 체리맛인가?",
                "음! 라즈베리맛인가?",
                "음! 크랜베리맛인가?",
                "음? 레드커런트맛인가?",
                "음! 딸기맛인가?",
                "음! 복분자인가?"
            ],
            "B" : [
                "음! 토마토맛인가!",
                "음! 석류맛인가!",
                "음... 파프리카맛인가...",
                "음??? 뭐야 이 맛은... 무슨 물감맛이나...",
                "음! 사과맛인가!",
                "음! 용과맛인가? 쓰읍... 애매하네.",
                "뭐야! 담백한 맛이 나는데?",
                "으앗! 매워..."
            ]
        },
        "hpFull" : {
            "S" : [
                "든든해!",
                "딱코!",
                "좋았어!",
                "!"
            ],
            "B" : [
                "!!!",
                "뭣!",
                "우와!",
                "야호!"
            ]
        },
        "hpOver" : {
            "S" : [
                "어이, 이거 더 먹지 마."
            ],
            "B" : [
                "앗! 넘친다!",
                "앗! 넘쳐흐른다...",
                "으앗! 아까워..."
            ]
        },
        "hpTooOver" : {
            "S" : [
                "아..앗... 아까워라...",
                "...어쩔 수 없지...",
                "히잉... 들고 다닐 수 있었는데...",
                "우우...",
                "아..."
            ],
            "B" : [
                "아.",
                "어?",
                "잇크.",
                "아니 잠깐만.",
                "엇"
            ]
        }
    },

    "df" : {
        "restorationed" : {
            "S" : [
                "으으... 깃털이 드디어 멀쩡해졌어...",
                "깃털이 다시 자라나고 있어!",
                "내 깃털들! 그리웠다구...",
                "깃털들아! 오랜만이야!"
            ],
            "B" : [
                "깃털이! 많이 자라났어!",
                "우와!",
                "회복되어간다!",
                "드디어!",
                "흐흐 깃털들아 그리웠어."
            ]
        },
        "dfFull" : {
            "S" : [
                "깃털에서 윤기가 돌아!",
                "깃털이 단단해졌어!",
                "모든 깃털이 온전해!",
                "좋았어!"
            ],
            "B" : [
                "우왓!",
                "이거지!",
                "내 깃털들을 뚫으려면 한참은 걸릴거다!",
                "쿡쿡... 난 강해졌지!"
            ]
        },
        "dfOver" : {
            "S" : [
                "충분해."
            ],
            "B" : [
                "깃털이 더 많아지진 않네.",
                "에잉, 깃털이 더 단단해지지도 않네...",
                "씁... 살짝 아까운걸."
            ]
        },
        "dfTooOver" : {
            "S" : [
                "깃털이 더 이상 단단해지지는 않는데?",
                "...? 아무일도 없는데?",
                "...? 오잉?",
                "깃털이 그대로네..."
            ],
            "B" : [
                "...이건 요리할걸.",
                "...이건 좀... 낭비가 큰데?",
                "...내가 왜... 이걸...",
                "아."
            ]
        }
    },
    "atk" : {
        "lowAtk" : {
            "S" : [
                "더... 더 필요하다구...",
                "요리실력을 끌어 올리기 위해...",
                "더 큰 힘...",
                "갈증나..."
            ],
            "b" : [
                "아직 요리가 쉽지 않다고!!!",
                "요리하기엔 너무 깊게 들어온 걸지도...",
                "요리해버리겠어...",
                "아직도 모자라....",
            ]
        },
        "hiAtk" : {
            "S" : [
                "요리할 시간이다.",
                "썰어주마.",
                "구워주마.",
                "튀겨주마.",
                "삶아주마.",
                "손질해주마."
            ],
            "B" : [
                "식재료를 부수고 조미료를 섞을 시간이군.",
                "네놈들을 고기 완자로 만들어주마.",
                "네놈들을 가니쉬로 만들어주마.",
                "네놈들을 드레싱으로 만들어주마.",
                "네놈들을 젓갈로 담궈주마.",
                "네놈들을 분자단위로 재해석해주마."
            ]
        }
    }
}
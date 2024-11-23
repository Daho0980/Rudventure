"""
누군가 말했었지. '저 너머에는 뭐가 있을까?' 라고.
그런데.. 저 너머랄 것은 별거 없었어.
그저 무한한 위기만이 도사렸지.
나는 그때 깨달았어. 이 곳에 들어온 이상 끝은 없다는 걸.

- Asháli qílumlî juó -
"""


lowHp:list[str] = [
    "게임은 이제 시작이다.",
    "이 정도면... 버틸 수 있어.",
    "이까짓 상처로는 내 앞길을 막아설 수 없다.",
    "이런, 죽음의 문턱이 또 다가오셨군?",
    "흥...",
    "하, 어떻게 산 거지?",
    "왜 나한테만 주마등이 안 스치는지 의문이란 말이야.",
    "재수가 없군.",
    "와우... 방금 건 좀 아팠어.",
    "쓰으으으으으으읍... 하아아아아...",
    "점점 숨 쉬기가 힘들어지고 있어.",
    "하아... 하아아...",
    "스치면 죽겠군.",
]

treasureRoom:dict[int,list[str]] = {
    0 : [
        "이런.. 여기서마저 운이 없을 줄이야.",
        "뭔가... 조촐하군.",
        "하아...",
        "허.",
        "이딴 걸 보물이라고 둔 거야?",
        "아무래도 이 안에는 거지들만 사는 게 분명해.",
        "젠장, 비었군.",
        "여기도 비었어.",
        "예상했어.",
        "더 나은 걸 바랐다면 죽어야겠지."
    ],
    1 : [
        "흠.",
        "그래도 없는 것 보단 낫군.",
        "나머지 두 개는 어디로 갔지?",
        "또 두 개를 훔쳐가셨군, 그래?",
        "나쁘지 않아.",
        "봐줄 만하군.",
        "애초에 이 상자들이 왜 여기에 있는지도 의문이란 말이야.",
        "살짝 모자란 지원 받은 셈 치지."
    ],
    2 : [
        "이래야 보물이지.",
        "모두 온전한 상태라니. 운이 좋아.",
        "진수성찬이로군.",
        "땡잡았어.",
        "Oivets zacmodlé lëd Aẽàíęzc!!",
        "오호라...",
        "아직도 멀쩡한 게 남아있을 줄 알았어."
    ]
}

defeat:dict[str,list[str]] = {
    "HL" : [
        "아아...",
        "이건 아니야.",
        "난 이런 걸 원하지 않았어.",
        "나한테 도대체 왜 그러는 거야...",
        "또 다시 한 번...",
        "너무 무모했군..."
    ],
    "HUL" : [
        "아아...",
        "아직 부족해.",
        "말도 안돼.. 내, 내가..?",
        "나한테 도대체 왜 그러는 거야...",
        "너무 배고파...",
        "움직일 힘이 없어...",
        "조금만 덜 날뛰었더라면..."
    ],
    "CO" : [
        "아아...",
        "크아아아아아아아악!!!!!!",
        "아, 아니야..!! 안돼!!!",
        "이래선 안 되는 거였잖아...",
        "끄아아아악......",
        "결국 이렇게 되는구나...",
        "수치스럽기 그지없구나...",
        "으아... 아..!! 아아아아악!!!"
    ]
}

victory:dict[int,list[str]] = {
    0 : [
        "...",
        "최악이군.",
        "...겨우 살았네.",
        "쯧.",
        "이러다 진짜 죽겠어."
    ],
    1 : [
        "또 같은 게 반복되겠군. 내려가고 또 내려가고...",
        "온 몸이 꼬챙이로 쑤셔지는 느낌이야..",
        "이번에도... 아주 거지같은 한 판이었어.",
        "지금 시간이 얼마나 지났었지?",
        "진절머리가 나는군.",
        "당연히 해야 할 일이었다."
    ],
    2 : [
        "나쁘지 않군.",
        "으, 이러다가 나도 편린의 일부가 되겠어.",
        "편린 따위는 나락에나 처박혀 있으라지.",
        "뭐, 또 내려가나?",
        "더 조심해서 나쁠 건 없지.",
        "빨리 벗어날 수나 있으면 좋겠군."
    ],
    3 : [
        "그래 이거야..",
        "하하하하하! 찢고 죽인다!!",
        "말도 못 할 만큼 즐거운 나락이었다.",
        "다음 층까진 더 갈 수 있겠어.",
        "여기 녀석들은 이상하게 예의가 바르군... 왜지?",
        "글라가트로프의 의지는 끊이지 않으리."
    ]
}

TIOTA:list[str] = [
    "으웨에에에에에에에에엑",
    "어째서...",
    "...상심이 크군.",
    "으, 입에 들어갔어.",
    "아야."
]

collide = {
    "animal" : {
        "cat" : [
            "?",
            "뭐야.",
            "아.",
            "아야.",
            "흥, 고양이인가.",
            "..."
        ],
        "catAttack" : [
            "아야.",
            "아.",
            "앗따가.",
            "씁.",
            "앗따.",
            "악!!!!"
        ]
    },
    "monster" : {

    }
}

# 좋다, 미개한 선지자여. 기어이 1/6의 확률을 뚫고 여기까지 도달했구나.
# 내 너를 위해 위대한 선물(맛있다)를 내리노니,
# 젤리곰이나 받아라 yeet
clayModelAnswer:list[str] = [
    "어찌됐건 고맙군.",
    "이 또한 그 사람의 염원이었으리라...",
    "...",
    "감사히 받겠다... 네가 이 말을 들을 진 잘 모르지만.",
    "...나락에서 편히 잠드소서."
]

start:list[str] = [
    "어디 한 번 들들 볶아보자고.",
    "이번을 마지막으로 만들어주겠다.",
    "완전 팔팔해.",
    "자신감이 솟아오르는군.",
    "목표는 간단해. 찾아내서, 죽인다.",
    "후우...",
    "이 망할 놈의 자식들을 아주 예뻐해 줘야겠어.",
    "이건 모두... 존속을 위해서야.",
    "마음 단단히 먹어라. 목숨은 하나다.",
    "..."
]

startWithCowardmode:list[str] = [
    "닥쳐.",
    "기분이 괜히 더럽군.",
    "빌어먹을...",
    "저질같은 환영인사 같으니.",
    "시끄러워.",
    "그 아가리 싸물어.",
    "저리 꺼져.",
    "언젠간 네 오장육부를 뽑아내주마."
]

loadsaveStart:list[str] = [
    "하... 다시 깨어나자마자 저 자식의 목소리를 들어야 한다니.",
    "저 ㅆ...",
    "환영 참 좆같게 하는군.",
    "...좀 어디 찌그러져 있으면 안 되나?",
    "죽인다. 무조건 죽이겠다.",
    "한껏 비웃어라. 난 이곳을 부숴버릴테니."
]

soliloquy:dict[str,list] = {
    "HL" : [
        "후우.. 후우우...",
        "뼈가 거의 대부분 박살난 느낌이야.",
        "숨이 가쁘군.",
        "피가 지혈이 안 되고 있어.",
        "피를 너무 많이 흘린 것 같아.",
        "한 번만 더 맞는다면 그 다음은 없을지도 모르겠군.",
        "아악!! 쓰으읍...",
        "이건 정말... 아프군."
    ],
    "HUL" : [
        "배가 좀 고픈데.",
        "아... 좀 있으면 굶어죽겠어.",
        "배에서 밥을 달라고 부추기는군.",
        "음식이 좀 필요하겠어... 아니면 구슬이라도.",
        "여긴 멀쩡한 식량이 없어도 너무 없군.",
        "이 벽, 먹을 수 있는 건가?",
        "잿가루라도 퍼먹고 싶을 심정이야.",
        "아무거나 좋으니 먹을 수 있는 거라면 다 내놔."
    ],
    "CO" : [
        "왠지 모르게 더 추워지고 있어.",
        "음산하군...",
        "죄악이 날 감싸오는군. 이대론 위험해.",
        "점점 저주에 물들고 있어.",
        "내 몸이 녹아내리는 게 느껴지는군.",
        "얼음 속에 있는 것만 같아.",
        "차갑군, 차가워...",
        "으윽...",
        "아주 토 나올 정도로 음산하군 그래.",
        "날 내버려둬..."
    ],
    "ELS" : [
        "...계속 생각하던 거지만 여긴 너무 추워.",
        "눈 앞이 어둡군.",
        "어깨가 뻐근한 것 같아.",
        "가끔은 이렇게 쉬는 것도 나쁘지 않지.",
        "이럴 때일수록 준비를 단단히 해야 한다.",
        "이 소리는... 허, 알 턱이나 없지.",
        "Qilumúd qhaüdle lháũ, Qůovémúd koüqle rícũ",
        "얼마나 이렇게 멀쩡하게 있을지 모르겠군."
    ]
}

enterinBattle:dict[int,list[str]] = {
    0 : [
        "싸울 시간이다.",
        "가보자고.",
        "모두 성불시켜주겠다...",
        "좋아. 줘팰 놈들이 더 많아졌어.",
        "그 꽉 막힌 속을 제대로 뚫어주마."
    ],
    5 : [
        "어... 이건 좀 많은데. 뭐, 상관없겠지. 덤벼라.",
        "너네가 아무리 막아선다 한들 나는 뚫으면 그만이지.",
        "물량공세라니, 나약하기 그지없군.",
        "하하하하하하하하!!!",
        "제대로 싸워야겠는데."
    ]
}

curseDecrease:dict[str,list[str]] = {
    "middleOver" : [
        "흐으... 아직이야. 더 필요해.",
        "저주가 빠져나갔는지도 모르겠군.",
        "아직도 고통이 느껴져.",
        "효과가 없어. 이 정도론 부족해.",
        "크으으윽..."
    ],
    "middleUnder" : [
        "후우. 이제야 살겠군.",
        "하하! 누가 죽는다 그랬지?",
        "이러다 죽는 거 아닌가 생각했어.",
        "뭐... 괜찮아.",
        "적어도 저주가 내 눈까지 침식하는 건 막았으니 됐어."
    ],
    "Under" : [
        "개운하군.",
        "이 정도는 버틸 수 있었는데 말이지.",
        "흠.",
        "음.",
        "Hez, od ióvlud éá"
    ]
}

getOrb:dict[str,dict[str,dict[int,list[str]]]] = {
    "hp" : {
        "hpLow" : {
            0 : [
                "아직... 부족해.",
                "겨우 이 정도로 몸이 회복될 리가 없지.",
                "여전히 힘들어.",
                "스치면 죽겠군. 아직도 말이야.",
                "이걸 좋아해야 하나?",
                "그럼 그렇지."
            ],
            1 : [
                "내 피통이 이렇게나 큰 줄 몰랐군.",
                "아... 아직 부족해.",
                "이젠 이걸로도 괜찮아지질 않는군.",
                "여전해.",
                "... 허."
            ]
        },
        "notHpLow" : {
            0 : [
                "겨우 살았군.",
                "그나마 나아.",
                "이거라도 있어서 다행이군.",
                "뭐... 괜찮아.",
                "목숨이 위험할 뻔 했어."
            ],
            1 : [
                "이제야 완전해지는 기분이군.",
                "그래 이 정도는 돼야지.",
                "만족스러워.",
                "맛은 없지만... 속이 든든해지는 느낌이야."
            ]
        },
        "hpFull" : {
            0 : [
                "딱 맞췄어.",
                "편안하구만.",
                "내가 아무리 결벽증은 아니더라도 기분은 좋군.",
                "이거지.",
                "캬... 완벽해."
            ],
            1 : [
                "이런 일은 드문데 말이지.",
                "언제 또 이런 느낌을 받아보겠어.",
                "딱 맞췄어. 무려 큰 체력 구슬로.",
                "이렇게 기분이 좋을 수가 없는데 말이야.",
                "역시 나야."
            ]
        },
        "hpOver" : {
            0 : [
                "아, 한계 이상으로 흡수했군.",
                "나머지는 버려지겠어.",
                "별 수 없지. 나머지는 소멸시킨다.",
                "아깝군.",
                "아..."
            ],
            1 : [
                "큰 구슬이라 좋긴 한데... 좀 넘었어.",
                "딱 알맞게 채워지길 바랐는데 말이지.",
                "뭔가 불쾌해졌어.",
                "너무... 기운이 넘치는군.",
                "에이..."
            ]
        },
        "hpTooOver" : {
            0 : [
                "잠깐, 이미 충분한데...",
                "...뭣하러 이걸 흡수하고 앉아있는 거지?",
                "내가 생각해도 이건 낭비군.",
                "충분해. 굳이 더 흡수할 필요 없어.",
                "흠."
            ],
            1 : [
                "아... 흡수하지 말 걸 그랬군.",
                "나중을 위해서 남길 걸 그랬어.",
                "잠깐, 내가 뭔 짓을 한거지?",
                "이런...",
                "하...",
                "아니, 심지어 그건 큰 구슬이었다고."
            ]
        }
    },

    "df" : {
        "restorationed" : {
            0 : [
                "그래도 이걸로 수복됐으니 됐어.",
                "최소한의 방어야.",
                "드디어 피부가 제 역할을 하는군.",
                "한 방에 털리진 않겠어. 적어도 말이야.",
                "설마 이게 끝이라곤 안 하겠지."
            ],
            1 : [
                "바로 이거야.",
                "제법 탄탄하구만.",
                "점점 회복되는군.",
                "좋아, 다시 돌아왔어.",
                "이제야 안심이 되네."
            ]
        },
        "dfFull" : {
            0 : [
                "딱 맞췄어.",
                "이거지.",
                "이제야 온전해졌군.",
                "이럴 때마다 기분이 좋다니까.",
                "잉여 구슬이 없군. 아주 좋아."
            ],
            1 : [
                "키야...",
                "딱 들어맞았군.",
                "이게 낭만이지.",
                "편린들이 이걸 깨부수려면 좀 걸릴 거야.",
                "어디 전설에나 나올 법한 완벽함이야."
            ]
        },
        "dfOver" : {
            0 : [
                "이미 풍족해.",
                "흠.",
                "엄.",
                "부족한 게 채워지긴 했다만...",
                "아까운 생각이 드는 건 어쩔 수 없다. 실제로 아까우니 말이야."
            ],
            1 : [
                "좀 남는데... 어쩔 수 없군.",
                "그저 아쉬울 따름이지.",
                "추가로 지니고 다닐 순 없겠어.",
                "아깝구만.",
                "너무 과하게 원했군."
            ]
        },
        "dfTooOver" : {
            0 : [
                "아... 젠장.",
                "굴러들어온 복을 제 발로 차버리다니...",
                "...도대체 왜 흡수한거람.",
                "......아 잠깐.",
                "어?"
            ],
            1 : [
                "막강한 손실이 발생했어.",
                "이걸로 살아남을 방법은 더 줄었겠지.",
                "아무리 내가 했다 해도 이건 너무하군.",
                "지금 내가 무슨 짓을 벌인거지...",
                "아."
            ]
        }
    },

    "atk" : {
        "lowAtk" : {
            0 : [
                "아... 좀 많이 실망스러운데.",
                "너무 적어.",
                "적어.",
                "더.",
                "티끌도 모으면 태산이라고 했지.",
                "정말 쥐똥만큼만 주는군 그래.",
                "헛된 희망이라도 심어주는 건가?",
                "강해진 줄도 모르겠어."
            ],
            1 : [
                "아직도 부족하다고?",
                "얼마나 깊이 내려온건지 상상도 안 되는군.",
                "뭔가 이걸로는 아직 상대하기 버거워.",
                "겨우 발견했는데도 이 정도라...",
                "마치 켜기도 전에 퀘이필이 폭발한 느낌이군. 맞아. 실망했어.",
                "뭘 원한거냐. 이건 결국 내 운에 따른 결과다."
            ]
        },
        "hiAtk" : {
            0 : [
                "이 정도면 됐어.",
                "충분하군.",
                "이거야...",
                "이제 사냥할 시간이다.",
                "하하! 압도적인 공격력에 무릎 꿇어라!",
                "이 정도는 돼야지."
            ],
            1 : [
                "이 정도면 건들자마자 날아가겠어.",
                "적어도 이번 층까지는 안심하고 패죽일 수 있겠군.",
                "과연... 이것이 힘이로군.",
                "압도적이야.",
                "뭐든지 부술 수 있을 것만 같아.",
                "좋아. 힘이 넘치는군."
            ]
        }
    }
}

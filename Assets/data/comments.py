"""
Asha : 누군가 말했었지. '저 너머에는 뭐가 있을까?' 라고.
Asha : 그런데.. 저 너머랄 것은 별거 없었어.
Asha : 그저 무한한 위기가 존재할 뿐.
Asha : 나는 그때 깨달았어. 이 곳에 들어온 이상 끝은 없다는 걸.
"""

from Assets.data.color import cColors as cc


lowHpComment:list[str] = [
    "게임은 이제 시작이다.",
    "이 정도면... 버틸 수 있어.",
    "이까짓 상처로는 내 앞길을 막아설 수 없다.",
    "이런, 죽음의 문턱이 또 다가오셨군?",
    "흥...",
    "하, 어떻게 산 거지?",
    "왜 나한테만 주마등이 안 스치는지 의문이란 말이야.",
    "재수가 없군.",
]

treasureRoomComment:dict[int,list[str]] = {
    0 : [
        "이런.. 여기서마저 운이 없을 줄이야.",
        "뭔가... 조촐하군.",
        "날 초대해놓고서 보답하는 게 겨우 이건가?",
        "허.",
        "이딴 걸 보물이라고 둔 거야?",
        "아무래도 이 안에는 거지들만 사는 게 분명해.",
        "젠장, 비었군.",
        "여기도 비었어."
    ],
    1 : [
        "흠.",
        f"그래도 어디 {cc['fg']['R']}다른 나락{cc['fg']['L']}에 계신 {cc['fg']['Y']}누구{cc['fg']['L']}보다는 낫군.",
        "나머지 두 개는 어디로 갔지?",
        "또 두 개를 훔쳐가셨군, 그래?",
        "나쁘지 않아.",
        "봐줄 만 해.",
        "애초에 이 상자들이 왜 여기에 있는지도 의문이란 말이지."
    ],
    2 : [
        "이래야 보물이지.",
        "모두 온전한 상태라니. 운이 좋아.",
        "진수성찬이로군.",
        "땡잡았어.",
        "Oivets zacmodle led Aeàtiézc!!",
        "오호라..."
    ]
}

defeatComment:dict[str,list[str]] = {
    f"hp 부족" : [
        "아아...",
        "이건 아니야.",
        "난 이런 걸 원하지 않았어.",
        "나한테 도대체 왜 그러는 거야...",
        "또 다시 한 번...",
        "너무 무모했군..."
    ],
    f"허기 부족" : [
        "아아...",
        "아직 부족해.",
        "이건 거짓말이야.. 내, 내가..?",
        "나한테 도대체 왜 그러는 거야...",
        "너무 배고파...",
        "움직일 힘이 없어...",
        "조금만 덜 날뛰었더라면..."
    ]
}

victoryComment:dict[int,list[str]] = {
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
        "여기 녀석들은 이상하게 예의가 바르군... 왜지?"
    ]
}

TIOTAComments:list[str] = [
    "으웨에에에에에에에에엑",
    "어째서...",
    "...상심이 크군.",
    "으, 입에 들어갔어.",
    "아야."
]
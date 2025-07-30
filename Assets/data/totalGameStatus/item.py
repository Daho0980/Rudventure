statRatioComments = {
    "durability" : {
        10 : "곧 부서질 것만 같다.",
        20 : "금 간 부분이 많다.",
        40 : "꽤 많이 사용된 것 같다.",
        70 : "이 정도면 충분히 쓸 만하다.",
        90 : "새것과 같다."
    },

    "infection" : {
        10 : "문제 없이 사용할 수 있다.",
        30 : "군데군데 저주가 침식된 곳이 보인다.",
        60 : "상당 부분에 저주 침식이 진행됐다.",
        80 : "멀쩡한 곳이 없다.",
        90 : "저주받았다."
    },

    "infinite" : {
        "durability" : "영구적이다.",
        "infection"  : "찬란하다."
    }
}

itemPlaceableBlock:tuple = (
    'floor', 'orbBox', 'squishy0', 'squishy1',
    'clayModel', 'deadClayModel', 'flower',
    'petal', 'corpse', 'blood', 'aorta',
    'venaCava', 'ashChip'
)

typeMark:dict[str,str] = {
    "tool"       : "ޛ도구",
    "weapon"     : "ރ무기",
    "consumable" : "&소모품"
}

originMark:dict[str,str] = {
    "badal"      : "신국 바달",
    "qantalotia" : "콴탈로티아",
    "ethlem"     : "에틀렘",
    "vamulhen"   : "바뮬헨",
    "samarGavim" : "사마르 가빔",
    "nimDraha"   : "님 드라하",
    "senixn"     : "세닉션"
}
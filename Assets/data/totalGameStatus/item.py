iids:dict[str,dict[str,str]] = {
    "tool" : {
        "ásotus" : 'Ⴔ'
    },
    "weapon" : {
        "animus" : '',
        "anima" : ''
    },
    "consumable" : {  }
}

statRatioComments = {
    "durability" : {
        10 : "곧 부서질 것만 같다.",
        20 : "금 간 곳이 많다.",
        40 : "꽤 사용된 것 같다.",
        70 : "이 정도면 쓸만하다.",
        90 : "거의 새 것과도 같다."
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
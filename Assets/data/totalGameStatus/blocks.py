ids:dict[int,str] = {
    -1 : ' ',  # 무적
    0 :  ' ',  # 바닥
    1 :  '██', # 벽
    2 :  '. ', # 문
    3 :  ' ',  # 가짜 바닥
    4 :  'É',  # 구슬 상자
    5 :  'F',  # 출구
    6 :  '☒',  # 상자
    7 :  'X',  # 상자 표적
    8 :  'O',  # 말랑이 1
    9 :  'o',  # 말랑이 2
    10 : 'o',  # 작은 체력 구슬
    11 : 'q',  # 작은 방어력 구슬
    12 : 'v',  # 작은 공격력 구슬
    13 : 'o',  # 작은 허기 구슬
    14 : 'ø',  # 작은 저주 구슬
    15 : 'O',  # 큰 체력 구슬
    16 : 'Q',  # 큰 방어력 구슬
    17 : 'V',  # 큰 공격력 구슬
    18 : 'O',  # 큰 허기 구슬
    19 : 'Ø',  # 큰 저주 구슬
    20 : '☷',  # 토용
    21 : '☷',  # 죽은 토용
    22 : '*',  # 꽃
    23 : '.',  # 꽃잎
    24 : '?',  # 아이템
    25 : ' ',  # 구멍
    26 : 'X',  # 시체
    27 : '░',  # 혈액

    200 : '빔', # 고양이

    300 : '@', # 0, 255, 10 & 플레이어 1
    301 : '&', # 0, 255, 10 & 플레이어 2

    400 : 'Y', # 저주를 씻어내는 신상
    401 : 'Y', # 오염된 저주를 씻어내는 신상

    501 : 'H', # 최대 체력 증가(대동맥)
    502 : 'U', # 최대 방어력 증가(대정맥)

    600 : '%', # 고통
    601 : '#', # 불안
    602 : '※', # 원망

    900 : ';'  # 잿조각
}

types:dict[int,str] = {
    0 : "block",
    1 : "entity",
    2 : "item"
}

bloodIcon:dict[int,str] = {
    5 : "██",
    4 : "█▓",
    3 : "▓▒",
    2 : "▒░",
    1 : "░",
}

orbIds:dict[str,dict[str,list[int]]] = {
    "size" : {
        "smallOne" : [10, 11, 12, 13, 14],
        "bigOne"   : [15, 16, 17, 18, 19]
    },
    "type" : {
        "hp"     : [10, 15],
        "def"    : [11, 16],
        "atk"    : [12, 17],
        "hunger" : [13, 18],
        "exp"    : [14, 19]
    }
}

monsterInteractableBlocks:dict = {
    "steppable" : {
        "maintainable"   : [0, 7],
        "unmaintainable" : [4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 26, 27, 501, 502, 900],
        "total"          : [0, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 26, 27, 501, 502, 900]
    },
    "unsteppable" : [-1, 1, 2, 3, 5, 6, 20, 21, 25, 200, 300, 301, 400, 401, 600, 601, 602],
    "breakable"   : [0, 4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 26, 27, 501, 502, 900]
}
interactableBlocks:dict = {
    "steppable" : {
        "maintainable"   : [0, 7],
        "unmaintainable" : [4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 26, 27, 501, 502, 900],
        "total"          : [0, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 26, 27, 501, 502, 900]
    },
    "unsteppable" : [-1, 1, 2, 3, 5, 6, 20, 21, 25, 200, 300, 301, 400, 401, 600, 601, 602],
    "explodable"  : [0, 4, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 22, 23, 24, 26, 27, 400, 401, 900]
}


enemyIds :list[int] = [600, 601, 602]
animalIds:list[int] = [200]
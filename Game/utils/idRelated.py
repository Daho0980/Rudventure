"""
Global Functions 중 IDRelated 옵션

    ``IDIncryption`` : `DungeonPos`와 `RoomPos` 데이터를 주로 활용해 ID화시켜 돌려줌, ID의 형식은 `Rud.Dy.Dx.room.Ry.Rx`와 같이 나타냄, 좌표값 밖에는 ID화할 수 없음

    ``IDDecryption`` : `IDIncryption`으로 만들어진 좌표 데이터를 복호화함, 앞에 꼭 Rud가 붙어야 ID로 인정
"""

def IDIncryption(DungeonPos:list, RoomPos=None):
    """
    `DungeonPos`와 `RoomPos` 데이터를 주로 활용해 ID화시켜 돌려줌, ID의 형식은 `Rud.Dy.Dx.room.Ry.Rx`와 같이 나타냄, 좌표값 밖에는 ID화할 수 없음

        `DungeonPos`(list) : `DungeonY`, `DungeonX` 데이터를 포함함, 아래와 같이 작성할 수 있음
            ex)
                if Dy == 3 and Dx == 5:
                    DungeonPos = [3, 5]

        `RoomPos`(list)    : `RoomY`, `RoomX` 데이터를 포함함, 아래와 같이 작성할 수 있으며 기본적으로 `None`으로 설정되어 있음
            ex)
                if Ry == 3 and Rx == 5:
                    RoomPos = [3, 5]

            또한 `Ry`, `Rx` 요소 중...
                리스트의 길이가 0이라면: `Ry`, `Rx` = '?', 
                '?', 리스트의 길이가 1이라면: `Ry`, `Rx` = `Ry`, '?', 
                RoomPos가 기본값이라면 모두 '?'로 표시됨
    """
    Dy, Dx = DungeonPos[0], DungeonPos[1]
    Ry = '?' if RoomPos == None or len(RoomPos) < 1 else RoomPos[0]
    Rx = '?' if RoomPos == None or len(RoomPos) < 2 else RoomPos[1]
    return f"Rud.{Dy}.{Dx}.room.{Ry}.{Rx}"

def IDDecryption(ID:str):
    """
    `IDIncryption`으로 만들어진 좌표 데이터를 복호화함, 앞에 꼭 Rud가 붙어야 ID로 인정

        `ID`(str) : `IDIncryption`으로 만들어진 좌표 데이터가 포함됨, 무조건 기입해야 함
    """
    if ID.startswith("Rud"):
        output:list = ID.split('.')
        del output[0]

        for i in range(len(output)):
            if output[i].isdigit(): output[i] = int(output[i])
        return output
def measure(text: str) -> int:
    """
    문자열의 실제 출력 너비를 반환합니다.
    
    이 함수는 실제로 출력되는 캐릭터의 너비를 구별하여
    합산 후 `int` 값을 반환합니다.

    이 함수는 어떤 문자열을 터미널에 출력했을 때 실제로
    차지하는 너비를 계산해야 할 때 사용합니다.

    매개변수:
        **str**: 길이를 계산할 문자열입니다.

    반환:
        계산된 문자열의 실제 출력 너비를 반환합니다.
    """

def cut(text:str, width:int, maintain:bool=True, ellipsis:bool=False, height:int=0) -> list[str]:...
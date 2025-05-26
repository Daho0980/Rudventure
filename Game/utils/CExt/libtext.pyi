def joineach(mainline: list[str], subline: list[str]) -> str:
    """
    두 리스트 내부의 문자열을 순차적으로 섞은 문자열을 반환합니다.

    이 함수는 `list[str]` **mainline**과 `list[str]` **subline**의
    요소를 각각 한 개씩 배치 후 문자열로 반환합니다.

    이 함수는 두 문자열의 순차 배열이 필요할 때 사용합니다.

    매개변수:
        **mainline**: 첫번째 리스트입니다. 이 문자열의 요소가
                  가장 먼저 배치됩니다.
        **subline**: 두번째 리스트입니다. 이 문자열의 요소가
                 mainLine 다음으로 배치됩니다.

    반환:
        순차적으로 섞인 문자열을 반환합니다.

    """
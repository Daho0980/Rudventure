MarkdownKinds = {
    0 : "\033[0m", # normal (end)
    1 : "\033[1m", # bold
    2 : "\033[4m", # underscore
    3 : "\033[5m", # blink
    4 : "\033[7m", # reversal
    5 : "\033[8m"  # invisible
}

def cMarkdown(Type:list[int]|int=0) -> str:
    """
    list 형식으로 여러개 쓸 수 있음

    `0` : 기본\n
    `1` : 두껍게\n
    `2` : 밑줄\n
    `3` : 깜빡임\n
    `3` : 배경색과 글자색 반전 아님말고\n
    `4` : 없음. 진짜 그냥 사라짐
    """
    return ''.join(map(lambda c: MarkdownKinds[c], Type)) if isinstance(Type, list) else MarkdownKinds[Type]
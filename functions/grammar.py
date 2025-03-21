_pstpos = {
    "obj" : ('을', '를'),
    "top" : ('은', '는'),
    "sub" : ('이', '가')
}

_attrform = {
    "mod" : ("이라는", "라는")
}


_coda  = lambda letter: (ord(letter)-44032)%28 == 0

def pstpos(word:str, category:str, pstposOnly:bool=False) -> str:
    """
    category(str) :
    ```
    obj -> 을/를
    top -> 은/는
    sub -> 이/가
    ```
    """
    pstp = _pstpos[category][_coda(word[-1])]
    return pstp if pstposOnly else f"{word}{pstp}"

def attrform(word:str, category:str, attrformOnly:bool=False) -> str:
    """
    category(str) :
    ```
    mod -> (이)라는
    ```
    """
    attrf = _attrform[category][_coda(word[-1])]
    return attrf if attrformOnly else f"{word}{attrf}"
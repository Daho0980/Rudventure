def getFace(curr:int, prior:int, default:str) -> str:
    ch = curr-prior
    return'l' if ch==1 else 'r'if ch==-1 else default
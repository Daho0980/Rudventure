from Chat import mainFunctions as mf


def say_0(text:str) -> bool:
    mf.addChat([text])
    return True

def say_1(text:str, colorKey:str) -> bool:
    mf.addChat(["", text, colorKey or 'E'])
    return True
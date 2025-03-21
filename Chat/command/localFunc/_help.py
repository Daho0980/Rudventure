from Chat import (
    status        as s,
    mainFunctions as mf
)
from functions.grammar import (
    attrform as af,
    pstpos   as pp
)


def help_0() -> bool:
    for command, explanation in s.commands['total'].items():
        mf.addChat([
            command, explanation,
            'R'
                if  command in s.commands['globals']
                and not s.serverConnection
            else 'F'
        ])

    return True

def help_1(mode:str) -> bool:
    try:
        for command, explanation in {key: value for key, value in s.commands['total'].items() if key in s.commands[mode]}.items():
            mf.addChat([command, explanation, 'R'if mode=="globals"and not s.serverConnection else'F'])

        return True
    
    except Exception as e:
        mf.error(f"'{mode}'{pp(mode,'top',True)} 잘못된 모드 형식입니다. 명령 모드는 locals 또는 globals로만 구분되어야 합니다.", e)
        return False
    
def help_2(command:str) -> bool:
    if explanation:=s.commands['total'].get(command):
        hmm = command in s.commands['globals'] and not s.serverConnection

        mf.addChat([command, explanation, 'R'if hmm else'F'])
        if hmm:
            mf.info("이 명령어는 현재 사용할 수 없습니다.")

        mf.addChat(["", "사용 방법 :", 'F'])
        if len(explanations:=s.commands['explanations'][command]) == 0:
            mf.addChat(["", f"    <아직 제공되지 않음>", 'R'])
        else:
            for line in explanations: mf.addChat(["", f"    {line}", 'Y'])

        return True
    
    else:
        mf.error(f"'{command}'{af(command,'mod',True)} 명령은 존재하지 않습니다.")
        return False
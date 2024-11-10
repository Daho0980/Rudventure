from Chat import (
    status        as s,
    mainFunctions as mf
)


def authorization_0(authority) -> bool:
    authorityName = s.authority['NTS'][(authority:=int(authority))]
    if authority in s.currentUserAuthority:
        mf.sendError(f"'{s.authority[authority]}' 권한은 이미 가지고 있는 권한입니다.")
        return False

    if authority in (0,1) and s.serverConnection and mf.direct("RGS", "s.gameRecord")[1][0]:
        mf.sendInfo("해당 권한은 게임에 영향을 줄 수 있으므로 육신 보존 및 사록 기록이 정지됩니다.")
        mf.sendInfo("육신 보존과 사록 기록을 재활성화하려면 죽어야 합니다.")
        mf.direct("RCC", "s.gameRecord = False")

    s.currentUserAuthority.add(authority)
    mf.sendOutput(f"'{authorityName}'이/가 부여되었습니다.")

    return True

def authorization_1(authority) -> bool:
    authorityName = s.authority['NTS'][(authority:=int(authority))]
    if authority not in s.currentUserAuthority:
        mf.sendError(f"'{authorityName}' 권한은 가지고 있지 않은 권한입니다.")
        return False
    
    if authority == 4:
        mf.sendError("guest 권한은 제거할 수 없습니다.")
        return False
    
    s.currentUserAuthority.remove(authority)
    mf.sendOutput(f"'{authorityName}'이/가 제거되었습니다.")
    
    return True

def authorization_2() -> bool:
    mf.sendOutput(f"현재 가지고 있는 권한은 [{', '.join(list(map(lambda a: s.authority['NTS'][a], s.currentUserAuthority)))}] 입니다.")
    return True

def authorization_3() -> bool:
    mf.sendOutput(f"존재하는 권한의 종류는 [{', '.join(list(map(lambda a: s.authority['NTS'][a], s.authority['NTS'].keys())))}] 입니다.")
    return True
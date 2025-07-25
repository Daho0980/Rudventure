from Chat              import mainFunctions as mf
from functions.grammar import pstpos        as pp


def status_0(status:str)-> bool:
    try:
        mf.output(f"현재 '{status[2:]}'는 {mf.direct('RGS', status)[1][0]}입니다.")
        return True
    
    except Exception as e:
        mf.error("상태 정보를 불러오는 데 실패했습니다.", e)
        return False
    
def status_1(status:str, value:str):
    try:
        if eval(mf.direct("RCC", f"{status} = {value}")[1]):
            mf.output(f"'{status[2:]}'{pp(status[2:],'sub',True)} '{value}'로 변경되었습니다.")
            return True
        
        else: 
            mf.error("상태 변경에 실패했습니다.")
            return False
    
    except Exception as e:
        mf.error("상태 변경 중 예기치 못한 오류가 발생했습니다.", e)
        return False
    
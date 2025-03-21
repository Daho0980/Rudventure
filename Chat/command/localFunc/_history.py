from Chat import (
    status        as s,
    mainFunctions as mf
)


def history_0() -> bool:
    mf.output(f"현재 히스토리 용량은 {len(s.history['chat'])}/{s.history['max']}입니다.")
    return True

def history_1(limit:str|int) -> bool:
    try:
        before = s.history['max']
        limit  = int(limit)

        if limit == before:
            mf.info("히스토리 용량이 달라지지 않았습니다.")
            return True
        elif limit <= 0:
            raise Exception("limit은 0 이하일 수 없습니다.")

        s.history['max'] = limit
        if len(s.history['chat']) > limit:
            s.history['chat'] = s.history['chat'][-limit:]
        
        mf.output(f"히스토리 용량이 {before} -> {limit}(으)로 {'증가'if (limit-before)>0 else'감소'}하였습니다.")

        return True
    
    except Exception as e:
        mf.error(f"limit은 1 이상의 int 타입 숫자여야만 합니다.", e)
        return False
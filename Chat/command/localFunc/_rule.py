from Chat import (
    rules         as r,
    mainFunctions as mf
)


def rule_0() -> bool:
    for scope, explanation in r.ruleScopes.items():
        mf.addChat([scope, explanation, 'F'])

    return True

def rule_1(scope:str) -> bool:
    try:
        for rule, allowance in eval(f"r.{scope}").items():
            mf.addChat([rule, str(allowance), 'F'])

        return True
    
    except Exception as e:
        mf.sendError(f"'{scope}'(이)라는 스코프는 존재하지 않습니다.", e)
        return False

# NOTE: the 'rulePath' variable will take something like this:
#           "scope.rule"(str)
def rule_2(rulePath:str) -> bool:
    scope, rule = rulePath.split('.')

    try:
        mf.sendOutput(f"현재 '{rulePath}'은/는 '{eval(f'r.{scope}["{rule}"]')}'입니다.")
        return True
    
    except Exception as e:
        mf.sendError(f"'{rulePath}'(이)라는 위치는 존재하지 않습니다.", e)
        return False

def rule_3(rulePath:str, allowance:str) -> bool:
    scope, rule = rulePath.split('.')

    try:
        if not isinstance(eval(allowance), bool):
            mf.sendError(f"'{allowance}'은/는 bool 형태의 값이 아닙니다.")
            return False
        allowance = eval(allowance)

        exec(f"r.{scope}['{rule}'] = {allowance}")
        mf.sendOutput(f"'{rulePath}'가 '{eval(f'r.{scope}["{rule}"]')}'로 변경되었습니다.")

        return True

    except Exception as e:
        mf.sendError(f"'{rulePath}'(이)라는 위치는 존재하지 않습니다.", e)
        return False
from Chat import (
    rules         as r,
    mainFunctions as mf
)
from functions.grammar import (
    attrform as af,
    pstpos   as pp
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
        mf.error(f"'{scope}'{af(scope,'mod',True)} 스코프는 존재하지 않습니다.", e)
        return False

# NOTE: the 'rulePath' variable will take something like this:
#           "scope.rule"(str)
def rule_2(rulePath:str) -> bool:
    scope, rule = rulePath.split('.')

    try:
        mf.output(f"현재 '{rulePath}'{pp(rulePath,'top',True)} '{eval(f'r.{scope}["{rule}"]')}'입니다.")
        return True
    
    except Exception as e:
        mf.error(f"'{rulePath}'{af(rulePath,'mod',True)} 위치는 존재하지 않습니다.", e)
        return False

def rule_3(rulePath:str, allowance:str) -> bool:
    scope, rule = rulePath.split('.')

    try:
        if not isinstance(eval(allowance), bool):
            mf.error(f"'{allowance}'{pp(allowance,'top',True)} bool 형태의 값이 아닙니다.")
            return False
        allowance = eval(allowance)

        exec(f"r.{scope}['{rule}'] = {allowance}")
        mf.output(f"'{rulePath}'{pp(rulePath,'sub',True)} '{eval(f'r.{scope}["{rule}"]')}'로 변경되었습니다.")

        return True

    except Exception as e:
        mf.error(f"'{rulePath}'{af(rulePath,'mod',True)} 위치는 존재하지 않습니다.", e)
        return False
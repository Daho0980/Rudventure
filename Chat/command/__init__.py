import re        ; import curses
from   collections import defaultdict

from Chat import (
    rules         as r,
    status        as s,
    mainFunctions as mf
)

from .localFunc  import *
from .globalFunc import *


DSRE = [r";\s*", r"\s*=\s*"]

sayFuncParams = ["text", "colorKey"]

playerStatus = {
    "total" : [
        "hp", "Mhp", "df", "Mdf", "atk", "hunger", "lvl", "Mlvl",
        "xp", "Mxp", "fairWind", "MFairWind", "ashChip",
        "critRate", "critDMG", "evasionRate"
    ],
    "percentage" : ["critRate", "evasionRate"]
}


def dataInterpretation(text:str) -> dict:
    items = re.split(DSRE[0], text)
    
    outputDict = defaultdict(lambda: None)
    for item in items:
        if re.search(DSRE[1], item):
            key, value = map(lambda data: data.strip().strip(';'), re.split(DSRE[1], item))
            outputDict[key] = value.strip('"').strip("'") # type: ignore
    
    return outputDict

def main(command):
    rawCommand = ' '.join(command)

    command[0] = command[0][1:]

    if command[0] in s.commands['globals'] and not s.serverConnection:
        mf.sendError(f"해당 명령어('{command[0]}')는 시스템이 독립된 상태에서 사용할 수 없습니다.")
        return
    match command[0]:
        # region Locals
        case "say":
            if len(command) <= 1:
                mf.sendError(f"{rawCommand}은/는 올바르지 않은 형식입니다.")
                return
            
            if command[1] == "-t":
                rawData = command[1] = ' '.join(command[2:])

                try:
                    if isinstance(textData:=dataInterpretation(command[1]), dict):
                        try:
                            command[0] = 'say_1'
                            command[1] = textData['text']
                            command[2] = textData['colorKey']

                            if None in textData.values():
                                deniedParams = map(lambda x: f"'{x}'", [key for key, _ in textData.items() if key not in sayFuncParams])
                                raise Exception(f"({', '.join(deniedParams)})은/는 존재하지 않는 매개변수입니다.")

                        except Exception as e:
                            mf.sendError(f"{rawData}은/는 올바르지 않은 형식입니다.", e)
                            return
                except Exception as e:
                    mf.sendError(f"{rawData}은/는 올바르지 않은 형식입니다.", e)
                    return
                
                command = command[:3]

            else:
                command[0] = "say_0"
                command[1] = ' '.join(command[1:])
                command    = command[:2]

        case "rule":
            match len(command[1:]):
                case 0: command[0] = 'rule_0'
                case 1: command[0] = 'rule_1'
                case 2:
                    command[0] = 'rule_2'
                    command[1] = '.'.join(command[1:])
                    command    = command[:2]

                case 3:
                    command[0] = 'rule_3'
                    command[1] = '.'.join(command[1:3])
                    allowance  = command[-1]
                    command    = command[:2]
                    command.append(allowance)

                case _:
                    mf.sendError(f"'{rawCommand}'은/는 올바르지 않은 형식입니다.")
                    return
                
        case "clear":
            if len(command[1:]):
                mf.sendError(f"'{rawCommand}'은/는 올바르지 않은 형식입니다.")
                return
            
            command[0] = 'clear_0'
            
        case "crash":
            curses.endwin()
            exit(0)

        case "history":
            match len(command[1:]):
                case 0:
                    mf.sendError(f"'{rawCommand}'은/는 올바르지 않은 형식입니다.")
                    return
                
                case 1:
                    match command[1]:
                        case "size":
                            command[0] = 'history_0'
                            command = command[:1]
                        case "resize":
                            mf.sendError(f"해당 명령에는 limit이 무조건 포함되어야 합니다.")
                            return

                        case _:
                            mf.sendError(f"'{command[1]}'은/는 존재하지 않는 명령입니다.")
                            return

                case 2:
                    match command[1]:
                        case "resize":
                            command[0] = 'history_1'
                            command[1] = command[2]
                            command    = command[:2]
                        
                        case _:
                            mf.sendError(f"'{command[1]}'은/는 존재하지 않는 명령입니다.")
                            return

                case _:
                    mf.sendError(f"'{rawCommand}'은/는 올바르지 않은 형식입니다.")
                    return

        case "help":
            match len(command[1:]):
                case 0: command[0] = 'help_0'
                case 1:
                    command[0] = 'help_1'if command[1]in('locals','globals')else 'help_2'
                case _: 
                    mf.sendError(f"'{rawCommand}'은/는 올바르지 않은 형식입니다.")
                    return
                
        case "authorization"|"auth":
            match len(command[1:]):
                case 1:
                    match command[1]:
                        case "current": command[0] = 'authorization_2'
                        case "list":    command[0] = 'authorization_3'
                        case _:
                            mf.sendError(f"'{command[1]}'은/는 존재하지 않는 명령입니다.")
                            return                            

                    command = command[:1]

                case 2:
                    match command[1]:
                        case "add":    command[0] = 'authorization_0'
                        case "remove": command[0] = 'authorization_1'
                        case _:
                            mf.sendError(f"'{command[1]}'은/는 존재하지 않는 명령입니다.")
                            return
                    
                    if command[2] not in s.authority['STN'].keys():
                        mf.sendError(f"'{command[2]}'은/는 존재하지 않는 권한입니다.")
                        return
                    
                    command[1] = str(s.authority['STN'][command[2]])
                    command    = command[:2]

                case _:
                    mf.sendError(f"'{rawCommand}'은/는 올바르지 않은 형식입니다.")
                    return
                
        # region Globals
        case "status":
            if command[2] not in playerStatus['total']:
                mf.sendError(f"{command[2]}라는 상태는 존재하지 않습니다.")
                return
            
            match len(command[1:]):
                case 2:
                    match command[1]:
                        case "get":
                            command[0] = 'status_0'

                            command[1] = f"s.{command[2]}"
                            command    = command[:2]
                                
                        case "set":
                            mf.sendError(f"'{rawCommand}'의 다음에는 int형식의 변경값이 와야 합니다.")
                            return

                        case _:
                            mf.sendError(f"'{command[1]}'은/는 존재하지 않는 명령입니다.")
                            return
                        
                case 3:
                    match command[1]:
                        case "set":
                            if command[2] in playerStatus['percentage'] and (int(command[3])<0 or int(command[3])>100):
                                mf.sendError(f"'{command[2]}'의 변경값은 100 초과이거나 0 미만일 수 없습니다.")
                                return
                            
                            elif not isinstance(eval(command[3]), int):
                                mf.sendError(f"변경값은 int여야만 합니다.")
                                return
                            
                            command[0] = 'status_1'

                            command[1] = f"s.{command[2]}"
                            command[2] = command[3]
                            command    = command[:3]

                        case _:
                            mf.sendError(f"'{command[1]}'은/는 존재하지 않는 명령입니다.")
                            return
                    
                case _:
                    mf.sendError(f"'{rawCommand}'은/는 올바르지 않은 형식입니다.")
                    return

        case _:
            mf.sendError(f"'{command[0]}'라는 명령어는 존재하지 않습니다.")
            return
    

    if 0 not in s.currentUserAuthority:
        requiredAuthorities = list(map(lambda a: s.authority['NTS'][a], set(s.commands['authorities'][command[0][:-2]][int(command[0][-1])])-set(s.currentUserAuthority)))
        if requiredAuthorities:
            mf.sendError(f"해당 명령어를 실행할 권한이 충족되지 않았습니다.")
            mf.sendError(f"필요한 권한 : {', '.join(requiredAuthorities)}")
            return
    
    execute = eval(f"{command[0]}")(*command[1:])

    if r.command['showCommandOutput'] and execute:
        mf.sendExplanation(f"'{rawCommand}'이/가 성공적으로 실행되었습니다.")
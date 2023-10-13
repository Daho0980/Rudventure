import os
import base64
import random
from   Packages.lib.data import status as s

def calcFormula():
    expressions = []
    nums        = []

    for setFormula in range(9):
        expressions.append('+' if random.randrange(0, 2) == 0 else '-')
        nums.append(random.randrange(1, 10))

    return [expressions, nums]

class converter:
    def encode(string):
        """
        `string`(list): rud 방식으로 인코딩할 문자열, 리스트 내 모든 문자열은 마지막에 \\n을 꼭 기입해야 함
        """
        encryptedData = []
        key        = calcFormula()
        for line in string:
            encryptedData.append([])

            # 1차(유니코드 숫자에서 3 빼기)
            for text in line: encryptedData[-1].append(ord(text)-3)
            # 2차(1차 base64 인코딩(유니코드 '.'.join()))
            b64StrData = base64.b64encode('.'.join(map(str, encryptedData[-1])).encode('ascii')).decode('utf-8')
            # 3차(base64 인코딩된 문자열을 이진(list)으로 변환)
            encryptedData[-1] = []
            for b64Text in b64StrData: encryptedData[-1].append(bin(ord(b64Text))[2:])
            # 4차(base64 재변환)
            encryptedData[-1] = base64.b64encode('.'.join(map(str, encryptedData[-1])).encode('ascii')).decode('utf-8')
            # 5차(계산공식을 이용한 base64 암호 난독화(16진), (key(2진)는 라인 끝에 단서로 남겨짐))
            target   = 0
            cFedLine = []
            for text in encryptedData[-1]:
                cFedLine.append(hex((ord(text) + key[1][target]) if key[0][target] == '+' else (ord(text)-key[1][target])))
                target += 1 if target < len(key[0])-1 else (len(key[0])-1)*-1
            cFedLine = '|'.join(map(str, cFedLine))
            # print(f"Input : \n\n\033[32m{encryptedData[-1]}\033[0m \n\nOutput : \n\n\033[31m{cFedLine}\033[0m\n\n")
            encryptedData[-1] = cFedLine
        # 마지막(key를 2진으로 변환)
        binaryKey = []
        for text in str(key): binaryKey.append(str(bin(ord(text)))[2:][::-1])
        encryptedData.append('-'.join(binaryKey))
                
        return encryptedData
    
    def decode(string):
        """
        `string`(list) : converter.encode()로만 변형된 코드만 받음
        """
        outputData = []
        key        = ""
        for binCode in string[-1].split('-'): key += str(chr(int(f"0b{binCode[::-1]}", 2)))
        print(key)
        key = eval(key)

        for line in string:
            if line != string[-1]:
                outputData.append([])

                # 알빠노
                unCFedLine = ""
                target     = 0
                for text in line.split('|'):
                    unCFedLine += chr(((int(f"{text}", 16)+key[1][target])) if key[0][target] == '-' else (int(f"{text}", 16)-(key[1][target])))
                    target += 1 if target < len(key[0])-1 else (len(key[0])-1)*-1
                outputData[-1] = unCFedLine
                # 1차(base64 복호화 및 이진(list)으로 분리)
                outputData[-1] = base64.b64decode(outputData[-1]).decode('utf-8').split('.')
                # 2차(이진(list)으로 저장된 데이터를 base64 방식으로 변환 후 유니코드(list)화)
                b64Str = ""
                for i in outputData[-1]: b64Str += chr(int(f"0b{i}", 2))
                outputData[-1] = base64.b64decode(b64Str).decode('utf-8').split('.')
                # 3차(유니코드(list(str))로 저장된 데이터를 사용 가능한 문자열로 재구성)
                resultStr = ""
                for char in outputData[-1]: resultStr += chr(int(char)+3)
                outputData[-1] = resultStr
        
        return outputData
    
    def changeExtention(name:str, beforeExt=".rud", afterExt=".json"):
        """
        정변환(기본값) : 
                beforeExt = ".rud"
                afterExt  = ".json"
        역변환 :
                beforeExt = ".json"
                afterExt = ".rud"
        """
        try:
            PATH = f"{s.TFP}Packages{s.s}saveFiles"
            os.rename(f"{PATH}{s.s}{name}{beforeExt}", f"{PATH}{s.s}{name}{afterExt}")
        except: print(f"\'{PATH}{s.s}{name}{beforeExt}\'(이)라는 경로는 존재하지 않습니다.")
        else  : print(f"파일 확장자 변환 완료 : \033[31m{name}{beforeExt}\033[0m -> \033[32m{name}{afterExt}\033[0m")
            
# example = converter.encode(["레포\n", "다호\n", "업로드\n"])
# print(f"input : \n\n{example}")
# print(f"output : \n\n{converter.decode(example)}")


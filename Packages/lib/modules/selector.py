from Packages.lib.data        import status      as s
from Packages.globalFunctions import clear, play

class selector:
    def Change2D(subtitle, maxLine): # 1차원 subtitle을 2차원으로 재배열
        newSubtitle   = [] # 2차원 배열로 변환될 subtitle
        subListRow    = -1 # 가로
        subListColumn = -1 # 세로
        while True:
            if subListColumn >= len(subtitle)-1: break
            else                               :
                newSubtitle.append([]) # 새로운 세로 배열셋 추가
                subListRow += 1 # 가로 추가
            for i in range(maxLine):
                subListColumn += 1 # 세로 추가
                if subListColumn == len(subtitle): newSubtitle[subListRow].append(' ') # 세로 배열셋 내 공백 옵션 새로 추가
                else                             : newSubtitle[subListRow].append(subtitle[subListColumn]) # 세로 배열셋 내 옵션 새로 추가
        return newSubtitle

    def lineSpaceMaker(lineSpace):
        output = ''

        for i in range(lineSpace): output += ' '
        return output

    def printSelect(title, subtitle, arrow, Enter, maxLine, lineSpace, subtitleValues, nowSelectColumn, nowSelectRow, tag):
        def positionOutput(subtitle, row, column):
            if row == len(subtitle)-1:
                row     = 0
                column += 1
            else: row += 1

            return row, column

        if isinstance(title, list): print(title[0] + Enter) # list형 title 방지
        else:                       print(title + Enter)

        row     = -1
        column  = 0
        Display = ""
        for i in range(maxLine):
            subtitleLine = ''
            for j in range(len(subtitle)):
                row, column   = positionOutput(subtitle, row, column)
                subtitleLine += (f'{arrow[row][column]} {subtitle[row][column]}{selector.lineSpaceMaker(lineSpace)}')
            Display += subtitleLine; Display += '\n'
        if subtitleValues != []: Display += f"{s.markdown([0,2,3])}\n    {subtitleValues[(maxLine*nowSelectRow)+nowSelectColumn]}"
        Display += tag
        print(Display)

    def Dropdown(title, subtitle = {'Why did you do...' : 'WHY...'}, color = 0, icon = '>', maxLine = 'max', lineSpace = 1, tag=''):
        subtitleKeys   = []
        subtitleValues = []
        Enter          = '\n'
        colors         = {
            0 : '0', # end
            1 : '41', # red
            2 : '100' # grey
        }
        PrintColorType = {
            1 : '38', # text color
            2 : '48' # bg color
        }
        if maxLine == 'max':         maxLine = len(subtitle)
        if maxLine >  len(subtitle): raise Exception('최대 세로 배열수는 subtitle 개수보다 많을 수 없습니다!')
        if isinstance(subtitle, dict):
            subtitleKeys = list(subtitle.keys())
            subtitleValues = list(subtitle.values())
        else:
            subtitleKeys = subtitle
        if   isinstance(title, list): Enter      = '' # title이 list면 title이랑 subtitle 사이의 공백 제거
        if   isinstance(color, int):  arrowColor = colors[color] # 화살표 기본색 간단설정
        elif isinstance(color, list): arrowColor = f'{PrintColorType[color[0]]};2;{color[1]};{color[2]};{color[3]}' # 세부 RGB 설정
        subtitleKeys = selector.Change2D(subtitleKeys, maxLine)
        a            = 0
        while True:
            if subtitleKeys[a] == '': # a번째 subtitle이 빈칸일 때
                if a == len(subtitleKeys) - 1: # 근데 그게 마지막일 때
                    subtitleKeys = {'Why did you do...' : 'WHY...'} # 이스터에그 생성
                    a            = 0
                    break
                else: a += 1 # 아니면 올리기
            else: break
        nowSelectColumn = a # 현재 세로 위치 최초 설정
        nowSelectRow    = 0
        arrow           = [] # 아이콘이 존재할 리스트
        for i in range(len(subtitleKeys)):
            arrow.append([])
            for j in range(maxLine): arrow[i].append(' ')
        while True: # 어쩔반복
            arrow[nowSelectRow][nowSelectColumn] = f'\033[{arrowColor}m{icon}' # 화살표 위치 설정
            if nowSelectRow        < len(subtitleKeys)-1:               arrow[nowSelectRow+1][nowSelectColumn] = f"\033[0m " # 다음 가로줄이 존재할 때: 다음 가로줄의 nowSelectColumn번째 요소를 기본색, 상태로 되돌린다(색 전염 방지)
            if nowSelectRow        > 0 and nowSelectColumn < maxLine-1: arrow[0][nowSelectColumn+1]            = f"\033[0m " # 이전 가로줄이 존재하고 맨 아래쪽 줄이 아닐 때: 첫 가로줄의 아랫칸을 기본색, 상태로 되돌린다(색 전염 방지22)
            if nowSelectColumn + 1 < maxLine:                           arrow[nowSelectRow][nowSelectColumn+1] = f"\033[0m " # 현재 위치 + 1이 subtitle 최대 개수보다 적을 때: 다음칸을 기본색, 상태로 되돌린다(색 전염 방지333)
            selector.printSelect(title, subtitleKeys, arrow, Enter, maxLine, lineSpace, subtitleValues, nowSelectColumn, nowSelectRow, tag)

            SNum, SNum1                          = 1, 0 # 가로, 세로 변환 정도값
            up, down, left, right                = ['w', 'W', 'ㅈ'], ['s', 'S', 'ㄴ'], ['a', 'A', 'ㅁ'], ['d', 'D', 'ㅇ']
            Input                                = input(f"{s.colors['end']}>>>")
            arrow[nowSelectRow][nowSelectColumn] = ' '
            if Input in up: # sublist 현재 위치 올리기
                while True:
                    if nowSelectColumn == 0     and nowSelectRow == 0: SNum, SNum1 = 0, 0
                    if nowSelectColumn-SNum < 0 and nowSelectRow > 0:
                        nowSelectColumn = maxLine - 1
                        SNum                      = 0
                        nowSelectRow             -= 1
                    if subtitleKeys[nowSelectRow - SNum1][nowSelectColumn - SNum] in ['', ' ']:
                        if nowSelectColumn - SNum < 0:
                            if nowSelectRow - SNum1 < 0:
                                SNum, SNum1 = 0, 0
                                break
                            else:
                                SNum   = 0
                                SNum1 += 1
                        else: SNum += 1
                    else: break
                nowSelectRow    -= SNum1
                nowSelectColumn -= SNum
                play(f'{s.TFP}Packages{s.s}sounds{s.s}select.wav')
                clear()
            elif Input in down: # sublist 현재 위치 내리기
                while True:
                    if nowSelectColumn == maxLine-1 and nowSelectRow == len(subtitleKeys)-1: SNum, SNum1 = 0, 0
                    if nowSelectColumn+SNum > maxLine-1: # 내렸을 때 maxLine-1보다 nowSelectColumn+SNum이 더 높을 때:
                        nowSelectColumn = 0
                        SNum            = 0
                        nowSelectRow   += 1
                    if subtitleKeys[nowSelectRow + SNum1][nowSelectColumn + SNum] == '' or\
                       subtitleKeys[nowSelectRow + SNum1][nowSelectColumn + SNum] == ' ': # 어어? 빈칸이네?
                        if nowSelectColumn + SNum+1 > maxLine-1: # 근데 행이 올라가면 끝나?
                            if nowSelectRow + SNum1+1 > len(subtitleKeys)-1: # 근데 열도 올라가면 끝나??
                                SNum, SNum1 = 0, 0
                                break
                            else:
                                SNum   = 0
                                SNum1 += 1
                        else: SNum += 1
                    else: break
                nowSelectRow    += SNum1
                nowSelectColumn += SNum
                play(f'{s.TFP}Packages{s.s}sounds{s.s}select.wav')
                clear()
            elif Input in left and nowSelectRow > 0:
                nowSelectRow -= 1
                play(f'{s.TFP}Packages{s.s}sounds{s.s}select.wav'); clear()
            elif Input in right and nowSelectRow < len(subtitleKeys)-1:
                nowSelectRow += 1
                play(f'{s.TFP}Packages{s.s}sounds{s.s}select.wav'); clear()
            elif Input == '': play(f'{s.TFP}Packages{s.s}sounds{s.s}get_item.wav'); break # enter
            else: clear() # 별 개같은거 칠 때 방지용
        clear() # 최종
        blankD = 0 # 공백 개수 변수 선언
        for i in range(0, nowSelectRow+1): # 처음부터 현재 위치까지 존재하는 공백 개수 확인
            for j in range(0, nowSelectColumn+1):
                if subtitleKeys[i][j] == '': blankD += 1
        return (maxLine*nowSelectRow)+nowSelectColumn+1-blankD # 최대 라인 x 현재 가로줄 위치 + 현재 세로줄 위치 + 1 - 공백 개수

# selector.Dropdown('Title', ['subtitle', 'subtitle1', 'subtitle2'])
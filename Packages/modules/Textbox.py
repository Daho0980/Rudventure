import unicodedata

def TextBox(Inp, Type=0, maxLine=100, fillChar=" ", distance=0):
        Display = ""
        Line = {0:["╔", "╗"], 1:["╚", "╝"]}
        Display += "\n"*distance
        Display += Line[0][0]+"═"*(maxLine)+Line[0][1]+"\n"
        Texts = Inp.split("\n")
        for i in range(len(Texts)):
            space = 0
            for j in range(len(Texts[i])):
                if unicodedata.east_asian_width(Texts[i][j]) in ['F', 'W']: space += 2
                else: space += 1
            FrontHalfSpace = int((maxLine-space)/2)
            BackHalfSpace  = int((maxLine-space)/2) if (maxLine-space)%2 == 0 else int((maxLine-space)/2)+1
            Display += ("║"+fillChar*FrontHalfSpace)+Texts[i]+(fillChar*BackHalfSpace+"║")+"\n"
        Display += Line[1][0]+"═"*(maxLine)+Line[1][1]
        Display += "\n"*distance
        return Display

# print(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox(TextBox("와! 이제 영어(asdf)든 한글이든 막 써도 박스가 안터진다!\n이히히\n역시 둥근모꼴이야.")))))))))))))))))))))

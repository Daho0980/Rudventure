import random
from   PIL      import Image, ImageDraw, ImageFont
from   datetime import datetime

from Assets.data         import status    as s
from Game.utils.graphics import escapeAnsi


ftColors:dict = {
        "B" :  (0,0,0),
        "M" :  (116,19,13),
        "G" :  (56,125,33),
        "O" :  (127,127,38),
        "N" :  (0,0,122),
        "P" :  (116,19,123),
        "T" :  (56,125,126),
        "S" :  (185,185,185),
        "G1" : (127,127,127),
        "R" :  (234,51,35),
        "L" :  (117,251,76),
        "Y" :  (255,255,85),
        "B1" : (0,0,245),
        "F" :  (234,51,247),
        "A" :  (117,251,253),
        "W" :  (243,243,243),

        "CR" : (151, 62, 230),
        "CU" : (89, 156, 235)
}

# 이미지 크기 및 배경 설정
x, y  = 650, 700
image = Image.new("RGB", (x, y), (0, 0, 0))
draw  = ImageDraw.Draw(image)
font  = ImageFont.truetype(f"{s.TFP}Assets{s.s}fonts{s.s}DungGeunMo.ttf", 20)

stringInserter = lambda ol, il, index: ol[:index]+il+ol[index:]

def textObfuscator(text, r=1) -> str:
    output = ""

    for _ in range(r):
      line = ""
      for char in text:
          randomScale = random.randrange(-5, 6)
          if ord(char)<=randomScale:
              if randomScale<=0: randomScale*=-1
              else:              continue
          line += chr(ord(char)+randomScale)
      output += f"\n{line}"
      
    return output[:-2]

random.seed(sum(map(lambda char: ord(char), s.name))+s.stage-s.killCount+(s.lvl*4)/int(datetime.now().strftime('%Y%m%d%H%M%S')))


text:str = f"""
           ╔════════════════════════╗
      ╔════║ 나락에서 편히 잠드소서 ║════╗
     ╔╝    ╚════════════════════════╝    ╚╗
     ╚══════════╝              ╚══════════╝

     

     이름 :
     사인 :

     내려간 층 :
     죽인 편린의 수 :
     받은 저주의 강도 :
"""
curse:str = "Qupldeði hijaįo katwaįzΩjim-halað hijaði jizok qil, qupldeði qilði liubeź Qoliði Qupldeði ceq, kobidði Qupldeði edvitł"
noise:str = f"{curse}{textObfuscator(curse, r=9)}"
line:str  = "━"*100

draw.text((80, 182),  text,                  font=font, fill=(214,222,235)      ) # text
draw.text((200, 350), s.name,                font=font, fill=ftColors['L']      ) # name
draw.text((200, 371), escapeAnsi(s.DROD[0]), font=font, fill=ftColors[s.DROD[1]]) # deadReason
draw.text((250, 413), str(s.stage),          font=font, fill=ftColors['Y']      ) # stage
draw.text((300, 434), str(s.killCount),      font=font, fill=ftColors['R']      ) # killCount
draw.text((320, 455), str(s.lvl),            font=font, fill=ftColors['F']      ) # level

draw.text((0, 595),  noise, font=font, fill=(214,222,235)) # downside bar
draw.text((0, -108), noise, font=font, fill=(214,222,235)) # upside bar
draw.text((0, 100),  line,  font=font, fill=(214,222,235)) # downside line
draw.text((0, 575),  line,  font=font, fill=(214,222,235)) # upside line

if s.ezMode:
    draw.text((255, 515), "with", font=font, fill=(214, 222, 235))
    draw.text((300, 515), "쫄",   font=font, fill=ftColors['R']  )
    draw.text((320, 515), "보",   font=font, fill=ftColors['Y']  )
    draw.text((349, 515), "모",   font=font, fill=ftColors['L']  )
    draw.text((369, 515), "드",   font=font, fill=ftColors['B1'] )


# 이미지 저장 
image.save(f"DeathLog{s.s}{datetime.now().strftime('%Y%m%d%H%M')}_{s.name}.png")
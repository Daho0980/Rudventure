import time
from   random    import randrange, choices, choice
from   threading import Thread

from .                           import Animal
from Assets.data.color           import cColors     as cc
from functions.grammar           import pstpos      as pp
from Game.entities.player        import event       as pev
from Game.entities.algorithms    import AStar, OPath
from Game.utils.system.tts       import TTS, TTC
from Game.utils.system.sound     import play
from Game.utils.system.block     import iset

from Assets.data import (
    totalGameStatus as s,
    comments        as c,
    flags           as f
)
from Game.entities import (
    player as p,

    event
)
from Game.core.system.io.logger import (
    addLog
)
from Game.core.system.data.dataLoader import (
    obj
)


cry = [
    "야옹.", "미야옹.", "애옹.",
    "왱옭.", "냐옭.", "맹.",
    "웽.", "녥.", "엙.",
    "믝.", "매앖."
]

comfortableCry = [
    "가르랑.", "고로롱.",
    "고롱 고롱.", "가르릉.",
    "갸릉."
]

catComments = {
    "requestHp" : [
        "츄르 '줘'.", "힘들어.", "나갈래.",
        "...줘."
    ],
    "requestMhp" : [
        "특제 츄르 '줘'.",
        "내놔.", "...줘."
    ],
    "chat" : [
        "(하품)",
        "야!옹", "고!로!롱", "고로롱...",
        "골골...", "졸ㄹ려.", "피곤해.",
        ],
    "attacked" : [
        "앩!", "먥!", "애옭!", "앵옭!",
        "아야!", "악!", "앍!"
    ],
    "complaint" : [
        "네가 해.", "귀찮아.", "나갈래.",
        "?", "안해.", "내가 왜?", "싫어.",
    ],
    "stress" : {
        "get" : [
            "으으윽..", "머리아파..", "불쾌해...",
            "거지같아...", "힘들어...", "으악 고통!"
        ],
        "lose" : [
            "한 층 개운해졌어.", "으음~", "아이 좋아.",
            "(하품)", "으으음~", "기분이 좋아졌어."
        ]
    },
    "spitOut" : [
        "켘켘.", "구웨엑..", "케헥.", "구웩.",
        "쿠웩.", "겍.", "구왁.", "에엙."
    ]
}

actionP = {
    "player" : {
        "prob" : 30,

        "say"       : [30, 70],
        "goToSide"  : 30,
        "attack"    : 40,
    },
    "else" : {
        "prob" : 70,

        "spinAround" : 25,
        "move"       : 50,
        "grooming"   : 10
    }
}

# region cat
class Cat(Animal):
    """
    고양이.\n
    애옹 ㅇㅇ
    """
    # region init section
    def __init__(self,
                 tribe         :str,
                 name          :str,
                 icon          :str,
                 ID            :str,
                 color         :str,
                 colorKey      :str,
                 tag           :str,
                 initFuncParams:list) -> None:
        super().__init__(tribe, name, icon, 
                         ID, color, colorKey,
                         tag, initFuncParams)

    def start(self,
              setHp  :int       ,
              setAtk :int       ,
              Dy     :int       ,
              Dx     :int       ,
              y      :list|int  ,
              x      :list|int  ,
              perm              ,
              loyalty:int     =-1) -> None:
        super().start(setHp, setAtk, Dy, Dx, y, x, perm)

        self.target        = None
        self.actionPurpose = None
        self.actionCount   = 0

        self.stressLvl = 1 # min=1, max=4
        self.stressPt  = 0 # min=0, max=100

        self.loyalty = min(max(0, loyalty), 10)
        
        self.camouflage = {
            "ash"  : 0,
            "hair" : 0,
            "dust" : 0
        }
        self.ashWeight = {
            "leg"  : 0,
            "side" : 0,
            "tail" : 0
        }

        self.attackPlayerCooltime = 0
        self.combo                = 0

        self.OPathData  = []
        self.statusData = {}

        self.voicePath = ("entity", "animal", "cat", "cloudy", "cry", "short")

        self.targetTag = ""

        self.ignoreCommand = False

        self.teleport()

    # region tools
    def teleport(self) -> None:
        roomGrid = s.Dungeon[self.Dy][self.Dx]['room']

        play("entity", "animal", "cat", "cloudy", "cry", "long")
        roomGrid[self.y][self.x] = obj(
            '-be', 'invincibleEntity',
            block=f"{cc['fg']['A']}O {cc['end']}"
        ); time.sleep(0.05)

        roomGrid[self.y][self.x] = obj(
            '-be', 'invincibleEntity',
            block=f"{cc['fg']['A']}{self.icon}{cc['end']}"
        ); time.sleep(0.05)

        roomGrid[self.y][self.x] = obj('-be', self.id,
            block=f"{self.color}{self.icon}{cc['end']}",
            id   =self.id,
            tag  =self.tag
        )
        time.sleep(0.05)
        play("entity", "animal", "cat", "teleport")

    def superTeleport(self) -> None:
        play("entity", "animal", "cat", "cloudy", "cry", "long")
        event.spawn(self.y, self.x, f"{self.color}{self.icon}{cc['end']}")
        play("entity", "animal", "cat", "teleport")

    def checkPlayerisHere(self) -> bool:
        if (self.Dy,self.Dx) == (s.Dy,s.Dx): return True
        self.resetAction()

        if self.stage != s.stage:
            self.setLoyalty()
            self.stepped = obj('-bb', 'floor')
            self.stage   = s.stage

        else: s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = self.stepped

        self.coolTime    = 0
        self.Dy, self.Dx = s.Dy, s.Dx

        for y, x in [
            (s.y-1,s.x  ),
            (s.y,  s.x+1),
            (s.y+1,s.x  ),
            (s.y,  s.x-1)
        ]:
            block = s.Dungeon[self.Dy][self.Dx]['room'][y][x]
            if self.perm.data[block['id']] & self.perm.STEP:
                self.y, self.x = y, x

                self.stepped = block\
                        if self.perm.data[block['id']]&self.perm.MAINTAIN\
                    else block['blockData']\
                        if block.get('blockData', False)\
                    else obj('-bb', 'floor')
                
                if self.stage != s.stage: self.superTeleport()
                else                    : self.teleport()

                return False

        while 1:
            DRP = s.Dungeon[self.Dy][self.Dx]['room']
            ry = randrange(1, s.roomData['maxHeight']-1)
            rx = randrange(1, s.roomData['maxWidth'] -1)
            
            if not self.perm.data[DRP[ry][rx]['id']] & self.perm.STEP:
                continue
            self.y, self.x = ry, rx

            break

        if self.stage != s.stage: self.superTeleport()
        else                    : self.teleport()

        return False

    def wait(self) -> None:
        self.coolTime -= 1
        
        if self.isFocused:
            self.damaged()
            if self.hp <= 0: self.coolTime = 0
            time.sleep(0.001)

        self.checkPlayerisHere()

    #region stress system
    def getStress(self, count:int=1) -> None:
        while (self.stressPt+count) > 100:
            if self.stressLvl == 4: break
            self.stressLvl += 1
            self.say(choice(catComments['stress']['get']))

            if count > self.stressPt: count -= self.stressPt
            else:                     count -= (100-self.stressPt)
            self.stressPt = 0
        self.stressPt += count
    
    def loseStress(self, count:int=1) -> None:
        while count > 0:
            if self.stressPt < count:
                if self.stressLvl == 1:
                    self.stressPt = 0
                    break
                count -= self.stressPt
                self.stressLvl -= 1
                self.stressPt   = 100
                self.say(choice(catComments['stress']['lose']))

            elif self.stressPt >= count:
                self.stressPt -= count
                break

    # region loyalty system
    def setLoyalty(self) -> None:
        lvl    = self.stressLvl
        tu, ou = self.loyalty-2, self.loyalty-1
        to, oo = self.loyalty+2, self.loyalty+1

        self.loyalty = 10 if lvl<=2 and oo>=10\
            else to       if (lvl+self.stressPt)==0\
            else oo       if lvl<=2\
            else 0        if lvl>2 and ou<=0\
            else tu       if lvl==4\
            else ou       if 2<lvl<4\
            \
            else self.loyalty

    # region action settings
    def setAction(self) -> None:
        if self.ignoreCommand: self.ignoreCommand = False
        
        if s.enemyCount:
            self.target        = "enemy"
            self.actionPurpose = "attack"

            return

        if  self.stressLvl>=2\
        and self.stressPt >=50\
        and randrange(0,2):
            self.target = "rest"

            return

        self.target = choices(
            ["else", "player"],
            weights=[
                actionP['else']['prob'],
                actionP['player']['prob']
            ],
            k=1
        )[0]

        match self.target:
            case "player":
                self.actionPurpose = choices(
                    ["say", "goToSide"] if self.attackPlayerCooltime\
                    else ["say", "goToSide", "attack"],
                    weights=[
                        actionP['player']['say'][1],
                        actionP['player']['goToSide']
                    ]\
                        if self.attackPlayerCooltime\
                    else [
                        actionP['player']['say'][0],
                        actionP['player']['goToSide'],
                        actionP['player']['attack'],
                    ],
                    k=1
                )[0]

            case "else":
                if sum(self.camouflage.values()) >= 100:
                    self.actionPurpose = "spitOut"
                    self.actionCount   = 1
                    
                    return
                
                self.actionPurpose = choices(
                    ["spinAround", "move", "grooming"],
                    weights=[
                        actionP['else']['spinAround'],
                        actionP['else']['move'],
                        actionP['else']['grooming']
                    ],
                    k=1
                )[0]

                match self.actionPurpose:
                    case "spinAround": self.actionCount = randrange(1 ,6 )
                    case "move":       self.actionCount = randrange(6 ,21)
                    case "grooming":   self.actionCount = randrange(10,21)     

    def resetAction(self) -> None:
        self.target        = None
        self.actionPurpose = None
        self.actionCount   = 0

        if self.OPathData:  self.OPathData  = []
        if self.statusData: self.statusData = {}

    # region functions
    def say(self                                                           ,
            text     :str                                                  ,
            voicePath:tuple=("entity","animal","cat","cloudy","cry","short")) -> None:
        addLog(
            f"{self.color}\"{text}\"{cc['end']}",
            duration=max(50, TTC(text)),
            colorKey=self.colorKey
        )

        Thread(
            target=lambda: TTS(
                text,
                voicePath=voicePath,
                useLvl   =False
            ),
            daemon=True
        ).start()

    def chattering(self) -> None:
        termArray = [5]*randrange(7,19)
        for _ in range(randrange(0, 4)):
            termArray[randrange(0,len(termArray))] = 30

        for term in map(lambda i: i/100, termArray):
            DRP = s.Dungeon[self.Dy][self.Dx]
            DRP['room'][self.y][self.x] = obj(
                '-be', self.id,
                block=iset(
                    f"{cc['bg']['A']}{self.icon}{cc['end']}",
                    Type=self.face
                ),
                tag=self.tag
            )
            time.sleep(0.03)
            DRP['room'][self.y][self.x] = obj(
                '-be', self.id,
                block=iset(
                    f"{self.color}{self.icon}{cc['end']}",
                    Type=self.face
                ),
                tag=self.tag
            )
            time.sleep(term)

        DRP['room'][self.y][self.x] = obj(
            '-be', self.id,
            block=iset(
                f"{self.color}{self.icon}{cc['end']}",
                Type=self.face
            ),
            tag=self.tag
        )

    def grooming(self) -> None:
        DRP = s.Dungeon[self.Dy][self.Dx]
        DRP['room'][self.y][self.x] = obj(
            '-be', self.id,
            block=iset(
                f"{cc['bg']['A']}{self.icon}{cc['end']}",
                Type=self.face
            ),
            tag=self.tag
        )
        time.sleep(randrange(1,14)/10)

        DRP['room'][self.y][self.x] = obj(
            '-be', self.id,
            block=iset(
                f"{self.color}{self.icon}{cc['end']}",
                Type=self.face
            ),
            tag=self.tag
        )

    def checkPWRest(self, stress) -> bool:
        if not self.checkPlayerisHere():
            self.getStress(stress*2)

            return True
        
        return False

    # region move code
    def move(self) -> None:
        global comfortableCry, cry
        global catComments

        DRP      = s.Dungeon[self.Dy][self.Dx]
        bfy, bfx = self.y, self.x

        if not self.target: self.setAction()

        if not self.coolTime:
            self.coolTime = randrange(750, 1500)+(200*self.stressLvl)
            match self.target:
                # region enemy
                case "enemy":
                    if not s.enemyCount:
                        self.resetAction()

                        return
                    
                    if self.actionPurpose == "attack":
                        if  s.target['tag'] != self.targetTag\
                        and s.target['attackable']\
                        and not self.ignoreCommand:
                            if choices([1,0],[self.loyalty,10-self.loyalty],k=1)[0]:
                                self.targetTag = s.target['tag']
                            else:
                                self.say(choice(catComments['complaint']))
                                self.ignoreCommand = True

                        if self.targetTag not in s.entityHashPool:
                            self.targetTag = ""
                            self.combo     = 0

                        if self.combo==0 and not randrange(0,4):
                            self.combo = randrange(2,7)

                        if not self.targetTag:
                            self.getStress(2)
                            addLog(
                                f"{self.color}{self.name}{cc['end']}{pp(self.name,'sub',True)} 사냥감을 찾았습니다...",
                                colorKey=self.colorKey
                            )
                            self.chattering()

                        if self.combo:
                            self.coolTime = int(self.coolTime/5)
                            self.combo   -= 1

                        while 1:
                            if not f.pause:
                                if not self.checkPlayerisHere(): break

                                if self.targetTag:
                                    path = AStar.forTag(
                                        (self.y, self.x),
                                        self.targetTag,
                                        self.perm.IDSet['step']
                                    )

                                else:
                                    path = AStar.main(
                                        (self.y, self.x),
                                        self.perm.IDSet['enemy'],
                                        self.perm.IDSet['step']
                                    )
                                    
                                if not path:
                                    self.getStress()
                                    if not randrange(0,10): self.say(choice(cry))
                                    self.resetAction()

                                    return
                                
                                elif self.perm.data[DRP['room'][path[0]][path[1]]['id']] & self.perm.ENEMY:
                                    self.loseStress(randrange(1,3))
                                    self.attack(path[0], path[1], ("entity", "animal", "cat", "slash"))

                                    if not self.targetTag:
                                        if DRP['room'][path[0]][path[1]]['type'] == 'entity':
                                            self.targetTag = DRP['room'][path[0]][path[1]]['tag']

                                    if choices([0,1],[55,45],k=1)[0]:
                                        for target in choices(["leg", "side", "tail"], [55, 30, 15], k=2):
                                            self.ashWeight[target] += 1
                                    self.resetAction()

                                    return
                                
                                elif DRP['room'][path[0]][path[1]]['id'] == 'invincibleEntity':
                                    self.getStress()
                                    if not randrange(0,10): self.say(choice(cry))

                                    return

                                else:
                                    bfy, bfx       = self.y, self.x
                                    self.y, self.x = path

                                super().step(bfy, bfx)

                            time.sleep(0.07)

                # region player
                case "player":
                    if self.attackPlayerCooltime > 0: self.attackPlayerCooltime -= 1
                    
                    match self.actionPurpose:
                        case "say":
                            if self.hp <= int(self.Mhp/2):
                                self.getStress()
                                text = choice(catComments['requestHp'])

                            elif int((self.hp/self.Mhp)*100)>= 80:
                                text = choice(catComments['requestMhp'])

                            else: text = choice(catComments['chat'])
                            self.say        (text)
                            self.resetAction()
                        
                        case "attack":
                            if not self.attackPlayerCooltime: self.attackPlayerCooltime = randrange(7,16)

                            addLog(
                                f"{self.color}{self.name}{cc['end']}{pp(self.name,'sub',True)} 당신을 노려봅니다...",
                                colorKey=self.colorKey
                            )
                            self.chattering()

                            while 1:
                                if not f.pause:
                                    if not self.checkPlayerisHere(): break

                                    path = AStar.main(
                                        (self.y, self.x),
                                        [300],
                                        self.perm.IDSet['step']
                                    )

                                    if not path:
                                        if not randrange(0,10):
                                            self.getStress  ()
                                            self.say        (choice(cry))
                                            self.resetAction()

                                            return
                                        
                                    elif DRP['room'][path[0]][path[1]]['id'] == 300:
                                        self.loseStress(10)
                                        self.attackPlayer(
                                            1,
                                            ("entity", "animal", "cat", "slash"),
                                            "장난이었는데..."
                                        )
                                        pev.say(choice(c.collide['animal']['catAttack']))
                                        self.resetAction()

                                        return
                                    
                                    else:
                                        bfy, bfx       = self.y, self.x
                                        self.y, self.x = path
                                        
                                    super().step(bfy, bfx)

                                time.sleep(0.07)
                        
                        case "goToSide":
                            while 1:
                                if not f.pause:
                                    if not self.checkPlayerisHere(): break

                                    path = AStar.main(
                                        (self.y, self.x),
                                        [300],
                                        self.perm.IDSet['step']
                                    )
                                    
                                    if not path:
                                        if not randrange(0,10):
                                            self.getStress  (2)
                                            self.say        (choice(cry))
                                            self.resetAction()

                                            return
                                        
                                    elif DRP['room'][path[0]][path[1]]['id'] == 300:
                                        self.loseStress (5)
                                        self.say        (choice(comfortableCry))
                                        self.resetAction()
                                        
                                        return
                                    
                                    else:
                                        bfy, bfx       = self.y, self.x
                                        self.y, self.x = path

                                    super().step(bfy, bfx)

                                time.sleep(0.2)

                # region else
                case "else":
                    if not self.actionCount:
                        self.loseStress (5)
                        self.resetAction()

                        return
                    
                    match self.actionPurpose:
                        case "move":
                            self.actionCount -= 1
                            ay, ax            = -1, -1
                            if sum([ay,ax])==-2 or (self.y,self.x)==(ay,ax):
                                while 1:
                                    ay = randrange(1, len(DRP['room']   )-1)
                                    ax = randrange(1, len(DRP['room'][0])-1)
                                    if not (self.perm.data[DRP['room'][ay][ax]['id']]&self.perm.STEP):
                                        continue

                                    break

                            if randrange(0,2):
                                self.x += 1\
                                        if  self.x<ax\
                                        and self.perm.data[DRP['room'][self.y][self.x+1]["id"]]&self.perm.STEP\
                                    else -1\
                                        if  self.x>ax\
                                        and self.perm.data[DRP['room'][self.y][self.x-1]["id"]]&self.perm.STEP\
                                    else  0
                                
                            else:
                                self.y += 1\
                                       if  self.y<ay\
                                       and self.perm.data[DRP['room'][self.y+1][self.x]["id"]]&self.perm.STEP\
                                    else -1\
                                       if  self.y>ay\
                                       and self.perm.data[DRP['room'][self.y-1][self.x]["id"]]&self.perm.STEP\
                                    else  0
                            
                            super().step(bfy, bfx)
                            self.coolTime = randrange(150, 300)+(100*self.stressLvl)

                        case "spinAround":
                            self.actionCount -= 1
                            if self.statusData:
                                radius = self.statusData['radius']
                                path   = self.statusData['path']
                                speed  = self.statusData['speed']

                            else:
                                radius = randrange(1,4)
                                while 1:
                                    path  = self.OPathData or OPath.main(radius, (self.y, self.x))
                                    speed = randrange(2,10)/100

                                    if path[0][0]<=0 or path[0][1]<=0:
                                        if radius == 1:
                                            self.getStress(3)
                                            self.actionCount = 0

                                            return
                                        
                                        radius -= 1
                                        continue
                                    break

                                self.statusData = {
                                    "radius" : radius,
                                    "path"   : path,
                                    "speed"  : speed
                                }
                                    
                            self.OPathData = path
                            gotoY, gotoX   = map(
                                lambda p: -1 if p<0 else 1 if p>0 else 0,
                                (path[0][0]-self.y, path[0][1]-self.x)
                            )
                            
                            while (self.y,self.x) != (path[0][0]-gotoY,path[0][1]-gotoX):
                                if not f.pause:
                                    if not self.checkPlayerisHere():
                                        self.actionCount = 0
                                        break

                                    blockID = DRP['room'][self.y+gotoY][self.x+gotoX]['id']
                                    if not self.perm.data[blockID] & self.perm.STEP:
                                        self.getStress(3)
                                        self.actionCount = 0
                                        play("entity", "animal", "cat", "collide")
                                        self.say(choice(catComments['attacked']))

                                        if blockID in ('player1', 'player2'):
                                            pev.say(choice(c.collide['animal']['cat']))

                                        break

                                    bfy, bfx  = self.y, self.x
                                    self.y   += gotoY
                                    self.x   += gotoX

                                    super().step(bfy, bfx)

                                time.sleep(speed)

                            for direction in path:
                                if not f.pause:
                                    if not self.checkPlayerisHere():
                                        self.actionCount = 0

                                        break

                                    blockID = DRP['room'][direction[0]][direction[1]]['id']
                                    if not self.perm.data[blockID] & self.perm.STEP:
                                        self.getStress(3)
                                        self.actionCount = 0
                                        play("entity", "animal", "cat", "collide")
                                        self.say(choice(catComments['attacked']))

                                        if blockID in ('player1', 'player2'):
                                            pev.say(choice(c.collide['animal']['cat']))

                                        break

                                    bfy, bfx       = self.y, self.x
                                    self.y, self.x = direction

                                    super().step(bfy, bfx)

                                time.sleep(speed)

                            self.coolTime = int(speed*100)\
                                    if self.actionCount>0\
                                else self.coolTime
                            
                        case "grooming":
                            if not sum(self.ashWeight.values()):
                                self.actionCount = 0
                                self.resetAction()

                                return

                            self.actionCount -= 1
                            addLog(
                                f"{self.color}{self.name}{cc['end']}{pp(self.name,'sub',True)} 그루밍 중입니다...",
                                colorKey=self.colorKey
                            )
                            
                            target = choices(
                                ["leg", "side", "tail"],
                                list(self.ashWeight.values()),
                                k=1
                            )[0]

                            self.grooming()
                            if self.ashWeight[target]:
                                self.ashWeight[target] -= 1
                                self.camouflage['ash'] += 1

                            self.camouflage['hair'] += randrange(1,5)
                            self.camouflage['dust'] += randrange(0,3)
                            self.coolTime = randrange(100,501)

                        case "spitOut":
                            for y, x in [
                                (self.y-1, self.x  ),
                                (self.y,   self.x+1),
                                (self.y+1, self.x  ),
                                (self.y,   self.x-1)
                            ]:
                                blockID = s.Dungeon[self.Dy][self.Dx]['room'][y][x]['id']
                                if self.perm.data[blockID] & self.perm.STEP:
                                    ty, tx = y, x

                                    break

                            else:
                                self.getStress(5)
                                self.resetAction()

                                return
                            
                            self.say(choice(catComments['spitOut']))
                            s.Dungeon[self.Dy][self.Dx]['room'][ty][tx] = obj('-bb',
                                str(choices(
                                    ('csOrbS', 'dfOrbS', 'atkOrbS'),
                                    list(self.camouflage.values()),
                                    k=1
                                )[0])
                            )
                            
                            self.camouflage = {k:0 for k in self.camouflage}
                            self.loseStress(5)
                            self.resetAction()

                # region rest
                case "rest":
                    addLog(
                        f"{self.color}{self.name}{cc['end']}{pp(self.name,'sub',True)} 자고 있습니다...",
                        colorKey=self.colorKey
                    )
                    stress = 0
                    while self.stressLvl!=1 and self.stressPt!=0:
                        if self.checkPWRest(stress): break

                        s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = obj(
                            '-be', self.id,
                            block=iset(
                                f"{cc['bg']['A']}{self.icon}{cc['end']}",
                                Type=self.face
                            ),
                            tag=self.tag
                        )
                        if self.checkPWRest(stress): break
                        time.sleep(1.5)
                        if self.checkPWRest(stress): break

                        s.Dungeon[self.Dy][self.Dx]['room'][self.y][self.x] = obj(
                            '-be', self.id,
                            block=iset(
                                f"{self.color}{self.icon}{cc['end']}",
                                Type=self.face
                            ),
                            tag=self.tag
                        )
                        if self.checkPWRest(stress): break
                        time.sleep(1.5)

                        self.loseStress(10); stress += 10

        else: self.wait()
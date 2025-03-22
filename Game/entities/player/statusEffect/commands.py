from Assets.data                 import totalGameStatus as s
from Assets.data.color           import cColors         as cc
from Game.core.system.logger     import addLog
from Game.core.system.dataLoader import obj
from Game.utils.system           import sound
from Game.utils.system.block     import iset


def main(effect, sequence):
    if effect['seq'] != sequence: return

    match effect['id']:
        case 1:
            s.steppedBlock = obj(
                '-bb', '27',
                block=iset(s.bloodIcon[1]),
                nbt  ={
                    "link"      : False,
                    "stack"     : 1
                },
                blockData=s.steppedBlock
            )
        
        case 600:
            if not effect['tick']%15 or effect['tick']==1:
                s.hp -= 1
                sound.echo(
                    "entity", "enemy", "pain", "growl",
                    feedback=50,
                    vVolume =65
                )
                sound.play("player", "hit")

                addLog(
                    f"{cc['fg']['F']}계속해서 이명이 들려옵니다...{cc['end']}",
                    colorKey='F'
                )

                s.DROD = [f"{cc['fg']['F']}신경성 쇼크{cc['end']}", 'F']
from Assets.data.color import cColors as cc

from Assets.data import (
    totalGameStatus as s,
    comments        as c
)


def main(data):
    SD = data['status']
    CD = data['comments']

    s.name      = SD['name']
    s.lightName = f"{cc['fg']['L']}{SD['name']}{cc['end']}"

    s.hp       = SD['hp']
    s.df       = SD['df']
    s.atk      = SD['atk']
    s.hgr      = SD['hgr']
    s.xp       = SD['xp']
    s.lvl      = SD['lvl']
    s.critDMG  = SD['critDMG']
    s.critRate = SD['critRate']
    s.ashChip  = SD['ashChip']

    s.Mhp  = SD['Mhp']
    s.Mdf  = SD['Mdf']
    s.Mxp  = SD['Mxp']
    s.Mlvl = SD['Mlvl']

    s.stage     = SD['stage']
    s.killCount = SD['killCount']

    s.bodyPreservationMode = SD['bodyPreservationMode']
    s.cowardMode           = SD['cowardMode']
    s.sanjibaMode          = SD['sanjibaMode']

    s.eids['player1']  = SD['playerIcon']
    s.playerDamageIcon = SD['playerDamageIcon']
    s.playerColor      = SD['playerColor']
    s.playerVoice      = SD['playerVoice']

    s.entityDataMaintained = SD['entityDataMaintained']
    
    c.lowHp               = CD['lowHp']
    c.treasureRoom        = CD['treasureRoom']
    c.defeat              = CD['defeat']
    c.victory             = CD['victory']
    c.TIOTA               = CD['TIOTA']
    c.collide             = CD['collide']
    c.clayModelAnswer     = CD['clayModelAnswer']
    c.start               = CD['start']
    c.startWithCowardmode = CD['startWithCowardmode']
    c.loadsaveStart       = CD['loadsaveStart']
    c.monologue           = CD['monologue']
    c.enterinBattle       = CD['enterinBattle']
    c.curseDecrease       = CD['curseDecrease']
    c.getOrb              = CD['getOrb']
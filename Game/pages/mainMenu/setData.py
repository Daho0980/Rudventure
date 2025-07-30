from Assets.data       import totalGameStatus as s
from Assets.data.color import cColors         as cc


def main(data):
    SD = data['status']

    s.name = SD['name']

    s.playerColor    = SD['playerColor']
    s.playerVoice    = SD['playerVoice']
    s.playerIdentity = SD['playerIdentity']
    s.lightName      = f"{s.playerColor}{SD['name']}{cc['end']}"

    s.eids['player1']  = SD['playerIcon']
    s.playerDamageIcon = SD['playerDamageIcon']

    s.stage     = SD['stage']
    s.killCount = SD['killCount']

    s.memory        = SD['memory']
    s.inventory     = SD['inventory']
    s.statusEffect  = SD['statusEffect']
    s.statusFormula = SD['statusFormula']

    s.hp       = SD['hp']
    s.df       = SD['df']
    s.atk      = SD['atk']
    s.hgr      = SD['hgr']
    s.xp       = SD['xp']
    s.lvl      = SD['lvl']
    s.ashChip  = SD['ashChip']

    s.Mhp  = SD['Mhp']
    s.Mdf  = SD['Mdf']
    s.Mhgr = SD['Mhgr']
    s.Mxp  = SD['Mxp']
    s.Mlvl = SD['Mlvl']

    s.critRate    = SD['critRate']
    s.critDMG     = SD['critDMG']
    s.evasionRate = SD['evasionRate']
    s.missRate    = SD['missRate']

    s.entityDataMaintained = SD['entityDataMaintained']
    s.gameRecord           = SD['gameRecord']

    s.cowardMode           = SD['cowardMode']
    s.sanjibaMode          = SD['sanjibaMode']
    s.bodyPreservationMode = SD['bodyPreservationMode']

    match s.playerIdentity:
        case "repo"  : from ..character import repo
        case "upload": from ..character import upload
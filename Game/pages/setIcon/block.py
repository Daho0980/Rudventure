from Assets.data.color import cColors as cc

from Assets.data import (
    totalGameStatus as s,
    markdown        as md
)


def main(func):
    def wrapper(*args):
        func(*args)

        s.bids['orbBox']   = f"{cc['fg']['Y']}É{cc['end']}"
        s.bids['exit']     = f"{cc['fg']['R']}F{cc['end']}"
        s.bids['squishy0'] = f"{cc['fg']['B1']}{md.cMarkdown(1)}O{cc['end']}"
        s.bids['squishy1'] = f"{cc['fg']['B1']}{md.cMarkdown(1)}o{cc['end']}"

        s.bids['hpOrbS']  = f"{cc['fg']['R']}o{cc['end']}"
        s.bids['dfOrbS']  = f"{cc['fg']['B1']}q{cc['end']}"
        s.bids['atkOrbS'] = f"{cc['fg']['L']}v{cc['end']}"
        s.bids['hgOrbS']  = f"{cc['fg']['Y']}o{cc['end']}"
        s.bids['csOrbS']  = f"{cc['fg']['F']}ø{cc['end']}"
        s.bids['hpOrbB']  = f"{cc['fg']['R']}O{cc['end']}"
        s.bids['dfOrbB']  = f"{cc['fg']['B1']}Q{cc['end']}"
        s.bids['atkOrbB'] = f"{cc['fg']['L']}V{cc['end']}"
        s.bids['hgOrbB']  = f"{cc['fg']['Y']}O{cc['end']}"
        s.bids['csOrbB']  = f"{cc['fg']['F']}Ø{cc['end']}"

        s.bids['deadClayModel'] = f"{cc['fg']['O']}☷{cc['end']}"

        s.bids['corpse'] = f"{cc['fg']['M']}X{cc['end']}"
        s.bids['blood']  = f"{cc['bg']['R']}░{cc['end']}"

        s.eids['player1'] = f"{cc['fg']['L']}@{cc['end']}" if s.eids['player1']=='@'else s.eids['player1']
        s.eids['player2'] = f"{cc['fg']['L']}&{cc['end']}"

        s.bids['normalStatue'] = f"{cc['fg']['A']}Y{cc['end']}"
        s.bids['cursedStatue'] = f"{cc['fg']['F']}Y{cc['end']}"

        s.bids['aorta'] = f"{cc['fg']['R']}H{cc['end']}"
        s.bids['venaCava'] = f"{cc['fg']['B1']}U{cc['end']}"

        s.bids['ashChip'] = f"{cc['fg']['G1']};{cc['end']}"

        s.bloodIcon = {
            5 : f"{cc['fg']['R']}██{cc['end']}",
            4 : f"{cc['fg']['R']}█▓{cc['end']}",
            3 : f"{cc['fg']['R']}▓▒{cc['end']}",
            2 : f"{cc['fg']['R']}▒░{cc['end']}",
            1 : f"{cc['fg']['R']}░{cc['end']}" ,
        }

    return wrapper
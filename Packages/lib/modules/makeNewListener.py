from pynput.keyboard          import Key, Listener
from Packages.lib             import quests, player
from Packages.lib.data        import status
from Packages.globalFunctions import fieldPrint, clear


def addListener():
    def key_press(key):
        if status.jpsf:
            if quests.quest(status.stage) != 1:
                inputs = (Key.up, Key.down, Key.left, Key.right)
                
                if key in inputs    : player.player.move(key, 1)
                if status.df > 0    : status.dfCrack = 0
                if status.frame == 0: clear(); fieldPrint()

    def key_release(key):
        from Packages.lib.system import options
        if status.yctuoh == False:
            if key == Key.esc:
                clear()
                print(f"{status.markdown([2, 3])}Enter를 한 번 눌러주세요{status.colors['end']}\n")
                options.menu()

    Listener(name="keyInput", on_press=key_press, on_release=key_release).start()
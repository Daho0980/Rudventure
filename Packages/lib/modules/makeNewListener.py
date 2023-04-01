from pynput.keyboard          import Key, Listener
from Packages.lib             import player
from Packages.lib.data        import status
from Packages.lib.system      import options


def addListener():
    def key_press(key):
        if status.jpsf and key in [Key.up, Key.down, Key.left, Key.right]:
            player.player.move(key, 1)

    def key_release(key):
        if status.yctuoh == False:
            if key == Key.esc  : options.menu()
            elif key == Key.tab: status.showDungeonMap = 1 if status.showDungeonMap == 0 else 0

    Listener(name="keyInput", on_press=key_press, on_release=key_release).start()
from pynput.keyboard          import Key, Listener
from Packages.lib             import player
from Packages.lib             import data
from Packages.lib.system      import options
from Packages.lib.system.globalFunc.sound import play

s, l = data.status, data.lockers

def addListener():
    def key_press(key):
        if l.jpsf == 1:
            print(s.lightName)
            if key in [Key.up, Key.down, Key.left, Key.right]: player.player.move(key, 1)

    def key_release(key):
        if l.jpsf == 1:
            if key == Key.esc  : options.menu()
            elif key == Key.tab:
                play("move_box")
                s.showDungeonMap = 1 if s.showDungeonMap == 0 else 0

    Listener(name="keyInput", on_press=key_press, on_release=key_release).start()
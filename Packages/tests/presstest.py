from pynput import keyboard

Input = ''

def on_press(key):
    print('Key %s pressed' % key)
    Input = key
    if key == keyboard.Key.esc: #esc 키가 입력되면 종료
        return False

def on_release(key):
    print('Key %s released' %key)
        
 # 리스너 등록방법1
with keyboard.Listener(
    on_press=on_press,
    on_release=on_release) as listener:
    listener.join()

print(Input)
import time
import pyxhook
import launchpad

log_file = 'log.txt'
LP = launchpad.Launchpad()
msg = ""
dic = {"Return":"\\n",
       "space":" ",
       "Tab":"\\t",
       "period":".",
       "colon":":",
       "semicolon":";",
       "Shift_L":"",
       "exclam":"!",
       "BackSpace":"BS",
       "asciicircum":"^",
       "asciitilde":"~",
       "minus":"-",
       "equal":"=",
       "Escape":"ESC",
       "parenleft":"(",
       "parenright":")",
       "bracketleft":"[",
       "bracketright":"]",
       "braceleft":"{",
       "braceright":"}",
       "greater":">",
       "less":"<",
       "quotedbl":"\"",
       "underscore":"_",
       "question":"?",
       "comma":",",
       "numbersign":"#",
       "dollar":"$",
       "percent":"%",
       "ampersand":"&",
       "apostrophe":"'",
       "plus":"+",
       "Shift_R":"",
       "slash":"/",
       "backslash":"\\",
       "Control_L":""}

def kbevent(event):
    global msg

    log = open(log_file, 'a')
    if event.Key in dic:
        ch = dic[event.Key]
    else:
        ch = event.Key
    msg += ch
    log.write(ch + "\n")

    # if event.Ascii == 94:
    #     log.close()
    #     hookman.cancel()

hookman = pyxhook.HookManager()
hookman.KeyDown = kbevent
hookman.HookKeyboard()
hookman.start()

while True:
    if len(msg) > 0:
        LP.LedScrollText(msg, 72, speed=7)
        msg = ""
        raw = None
        while raw == None:
            raw = LP.ReadRaw()
            time.sleep(0.01)
    time.sleep(0.01)

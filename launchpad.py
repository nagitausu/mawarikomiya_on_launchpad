import rtmidi2
import time

MAX_C = 63; MIN_C = 0
OFFSET = 1

class Launchpad():

    def __init__(self):
        self.midi_in = rtmidi2.MidiIn()
        self.midi_out = rtmidi2.MidiOut()

        device_name = "Launchpad MK2"
        try:
            index = self.midi_in.ports_matching(device_name + "*")[0]
            self.midi_in.open_port(index)
            self.midi_out.open_port(index)
            print("Port opened.")
        except IndexError:
            raise(IOError("Port not found."))

    def __del__(self):
        self.Reset()
        self.Close()
        print("Port terminated.")

    def Close(self):
        self.midi_in.close_port()
        self.midi_in = None
        self.midi_out.close_port()
        self.midi_out = None

    def ReadRaw(self):
        msg = self.midi_in.get_message()
        return msg

    def ReadXY(self):
        msg = self.ReadRaw()
        if msg:
            if not (msg[0] == 144 or msg[0] == 176):
                return None
            if msg[1] >= 104:
                x = 0
                y = msg[1] - 104
            else:
                x = (99 - msg[1]) // 10 - OFFSET
                y = (msg[1] - 1) % 10
            return [x, y, msg[2] // 127]
        else:
            return None

    def LedScrollText(self, text):
        # TODO: Fix midi library to take array for send_sysex()
        if text == "YOU WIN!!":
            self.midi_out.send_sysex(0, 32, 41, 2, 4, 20, 79, 0, 4, 89, 79, 85, 32, 87, 73, 78, 33)
        elif text == "YOU LOSE...":
            self.midi_out.send_sysex(0, 32, 41, 2, 4, 20, 72, 0, 4, 89, 79, 85, 32, 76, 79, 83, 69, 46, 46, 46)

    def LedCtrlRaw(self, number, red, green, blue):
        if (number > 89 and number < 104) or number < 0 or number > 111:
            return
        red = max(MIN_C, min(MAX_C, red))
        green = max(MIN_C, min(MAX_C, green))
        blue = max(MIN_C, min(MAX_C, blue))
        self.midi_out.send_sysex(0, 32, 41, 2, 16, 11, number, red, green, blue)

    def LedCtrlXY(self, x, y, red, green, blue):
        if x < 0 or x > 8 or y < 0 or y > 8:
            return
        x += OFFSET
        if x == 0:
            number = 104 + y
        else:
            number = 91 - (10 * x) + y
        self.LedCtrlRaw(number, red, green, blue)

    def LedAllOn(self, colorcode):
        self.midi_out.send_sysex(0, 32, 41, 2, 24, 14, colorcode)

    def Reset(self):
        self.LedAllOn(0)

if __name__ == "__main__":
    from threading import Timer
    from os import _exit as exit
    LP = Launchpad()

    # Read test
    # t = Timer(3, exit, args=(1, ))
    # t.start()
    # while True:
    #     time.sleep(0.001)
    #     msg = LP.ReadXY()
    #     if msg is not None:
    #         print(msg)

    # Write test
    for i in range(3):
        LP.LedCtrlXY(1, 0, 63, 63, 0)
        time.sleep(1)
        LP.LedCtrlXY(1, 0, 0, 0, 0)
        time.sleep(1)

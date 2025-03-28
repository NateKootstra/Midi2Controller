import threading

import mido
import pyvjoy

selected = None
options = mido.get_input_names()
print("MIDI Inputs:")
if len(options) > 0:
    print()
for i, option in enumerate(options):
    print(str(i + 1) + ". " + option)
print()
if len(options) == 0:
    print("No MIDI Inputs found.")
    exit()
elif len(options) == 1:
    print("Input (1):")
else:
    print("Input (1-" + str(len(options)) + ")")
selected = mido.open_input(options[int(input()) - 1])
class AkaiMpkMini:
    device = None
    
    pads = None
    black = None
    
    def __init__(self, device):
        self.device = device
        self.pads = [False, False, False, False, False, False, False, False]
        self.black = [False, False, False, False, False, False, False, False, False, False]
        self.blackIDs = { 49 : 0, 51 : 1, 54 : 2, 56 : 3, 58 : 4, 61 : 5, 63 : 6, 66 : 7, 68 : 8, 70 : 9}
        
    def update(self):
        for event in self.device:
            if "note" in dir(event):
                if event.note in self.blackIDs.keys():
                    if event.type == "note_on":
                        self.black[self.blackIDs[event.note]] = True
                    else:
                        self.black[self.blackIDs[event.note]] = False
            elif "program" in dir(event):
                pass
            elif "control" in dir(event):
                if event.control >= 16 and event.control <= 23:
                    self.pads[event.control - 16] = not self.pads[event.control - 16]
                
    def startMonitor(self):
        self.thread = threading.Thread(target=self.update)
        self.thread.start()
        
    def getPads(self):
        return self.pads
    
midi = AkaiMpkMini(selected)

midi.startMonitor()

joydevice = pyvjoy.VJoyDevice(1)

oldPads = midi.pads.copy()
oldBlack = midi.black.copy()
while True:
    print(midi.black)
    if not midi.pads == oldPads:
        oldPads = midi.pads.copy()
        for i,pad in enumerate(midi.pads):
            joydevice.set_button(i + 1, int(pad))
    if not midi.black == oldBlack:
        oldBlack = midi.black.copy()
        for i,black in enumerate(midi.black):
            joydevice.set_button(i + 9, int(pad))
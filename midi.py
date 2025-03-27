import threading

import mido

selected = None
options = mido.get_input_names()
for i, option in enumerate(options):
    print(str(i + 1) + ". " + option)
selected = mido.open_input(options[int(input()) - 1])
    
class AkaiMpkMini:
    device = None
    
    pads = None
    
    def __init__(self, device):
        self.device = device
        self.pads = [False, False, False, False, False, False, False, False]
        
    def update(self):
        for event in self.device:
            if "note" in dir(event):
                pass
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

print(midi.pads)
oldPads = midi.pads
while True:
    print(midi.pads)
    if not midi.pads == oldPads:
        print(midi.pads)
        oldPads = midi.pads
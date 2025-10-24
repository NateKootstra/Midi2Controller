import evdev
import pyvjoy


controller = [evdev.InputDevice(path) for path in evdev.list_devices()][-1]

print(controller.name)

controllerIDs = { 288 : 1, 295 : 2, 291 : 3, 293 : 4, 289 : 5, 292 : 6, 290 : 7, 294 : 8, 296 : 9, 297 : 10}

center = False
buttons = [False for i in range(11)]

joydevice = pyvjoy.VJoyDevice(2)

for event in controller.read_loop():
    if not (event.type == 0 or event.type == 4):
        if event.type == 3 and event.value == 255:
            buttons[0] = True
        elif event.type == 3 and event.value == 177:
            buttons[0] = False
        elif event.type == 1:
            buttons[controllerIDs[event.code]] = event.value == 1
        print(buttons)
    for i in range(11):
        joydevice.set_button(i + 1, int(buttons[i]))


import mido

selected = None
options = mido.get_input_names()
for i, option in enumerate(options):
    print(str(i + 1) + ". " + option)
selected = mido.open_input(options[int(input()) - 1])
    
while True:
    for msg in selected:
        print(str(msg))
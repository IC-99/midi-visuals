import pygame.midi as midi

midi.init()

print(midi.get_init())

print(midi.get_default_input_id())

print(midi.get_device_info(1))

input = midi.Input(1, 256)
create = False

while True:
    if input.poll():

        received = input.read(10)        
        
        for rec in received:
            if rec[0][0] != 248 and rec[0][1] == 72:
                create = not create
                print(create)
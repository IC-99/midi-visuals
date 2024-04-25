import pygame.midi as midi

midi.init()

print(midi.get_init())

print(midi.get_default_input_id())

print(midi.get_device_info(midi.get_default_input_id()))

input = midi.Input(midi.get_default_input_id(), 256)
create = False

while True:
    if input.poll():
        received = input.read(10)        
        for rec in received:
            if rec[0][0] == 144 or rec[0][0] == 128:
                create = not create
                print(create)
                if create:
                    print(rec[0])
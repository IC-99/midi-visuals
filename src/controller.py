import pygame.midi as midi
import random

class Midi_controller:

    def __init__(self, buffer_size) -> None:
        self.midi_input = None
        self.commands = [False] * 61
        self.velocities = [0] * 61
        self.colors = [(0, 0, 0)] * 61
        midi.init()
        if midi.get_init():
            self.midi_input = midi.Input(midi.get_default_input_id(), buffer_size)
        else:
            print('error while opening midi device')

    def get_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def read(self):
        try:
            if self.midi_input.poll():
                received = self.midi_input.read(10)
                for rec in received:
                    if rec[0][0] == 144 or rec[0][0] == 128:
                        self.commands[rec[0][1] - 36] = not self.commands[rec[0][1] - 36]
                        #print(self.commands[:20])
                        if self.commands[rec[0][1] - 36]:
                            self.velocities[rec[0][1] - 36] = rec[0][2]
                            self.colors[rec[0][1] - 36] = self.get_random_color()
                            #print(self.velocities[:20])
        except Exception as e:
            print('errore:', e)
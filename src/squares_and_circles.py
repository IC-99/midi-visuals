import cv2
import numpy as np
import pygame.midi as midi
import random

midi.init()
try:
    input = midi.Input(midi.get_default_input_id(), 256)
except:
    pass

# Definisci le dimensioni del video e il colore del cubo
video_width = 1920
video_height = 1080

# Inizializza il video
video = cv2.VideoWriter('cubo.mov', cv2.VideoWriter_fourcc(*'XVID'), 30, (video_width, video_height))

commands = [False] * 61
velocities = [0] * 61
colors = [(0, 0, 0)] * 61

square_size = 600
squares_gap = 200
p1_square1 = (video_width // 2 - squares_gap // 2 - square_size, (video_height - square_size) // 2)
p2_square1 = (p1_square1[0] + square_size, p1_square1[1] + square_size)

p1_square2 = (video_width // 2 + squares_gap // 2, (video_height - square_size) // 2)
p2_square2 = (p1_square2[0] + square_size, p1_square2[1] + square_size)

circle_gap = square_size // 6
circle_margin = 0.8
circle_ray = int((square_size // 6) * circle_margin)
p_circle1 = (p1_square1[0] + circle_gap, p1_square1[1] + circle_gap)
p_circle2 = (p1_square1[0] + circle_gap * 3, p1_square1[1] + circle_gap)
p_circle3 = (p1_square1[0] + circle_gap * 5, p1_square1[1] + circle_gap)
p_circle4 = (p1_square1[0] + circle_gap, p1_square1[1] + circle_gap * 3)
p_circle5 = (p1_square1[0] + circle_gap * 3, p1_square1[1] + circle_gap * 3)
p_circle6 = (p1_square1[0] + circle_gap * 5, p1_square1[1] + circle_gap * 3)
p_circle7 = (p1_square1[0] + circle_gap, p1_square1[1] + circle_gap * 5)
p_circle8 = (p1_square1[0] + circle_gap * 3, p1_square1[1] + circle_gap * 5)
p_circle9 = (p1_square1[0] + circle_gap * 5, p1_square1[1] + circle_gap * 5)

p_circle10 = (p1_square2[0] + circle_gap, p1_square1[1] + circle_gap)
p_circle11 = (p1_square2[0] + circle_gap * 3, p1_square1[1] + circle_gap)
p_circle12 = (p1_square2[0] + circle_gap * 5, p1_square1[1] + circle_gap)
p_circle13 = (p1_square2[0] + circle_gap, p1_square1[1] + circle_gap * 3)
p_circle14 = (p1_square2[0] + circle_gap * 3, p1_square1[1] + circle_gap * 3)
p_circle15 = (p1_square2[0] + circle_gap * 5, p1_square1[1] + circle_gap * 3)
p_circle16 = (p1_square2[0] + circle_gap, p1_square1[1] + circle_gap * 5)
p_circle17 = (p1_square2[0] + circle_gap * 3, p1_square1[1] + circle_gap * 5)
p_circle18 = (p1_square2[0] + circle_gap * 5, p1_square1[1] + circle_gap * 5)


circles = [p_circle1, p_circle2, p_circle3, p_circle4, p_circle5, p_circle6, p_circle7, p_circle8, p_circle9, p_circle10, p_circle11, p_circle12, p_circle13, p_circle14, p_circle15, p_circle16, p_circle17, p_circle18]

def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def draw_circle(command):
    r, g, b = colors[command]
    r = int(r * velocities[command] / 127)
    g = int(g * velocities[command] / 127)
    b = int(b * velocities[command] / 127)
    cv2.circle(frame, circles[command % 18], circle_ray, (r, g, b), -1)

# Ciclo per generare ogni frame del video
while True:

    # Leggi input midi se presenti
    try:
        if input.poll():
            received = input.read(10)

            for rec in received:
                if rec[0][0] == 144 or rec[0][0] == 128:
                    commands[rec[0][1] - 36] = not commands[rec[0][1] - 36]
                    print(commands[:20])
                    if commands[rec[0][1] - 36]:
                        velocities[rec[0][1] - 36] = rec[0][2]
                        colors[rec[0][1] - 36] = get_random_color()
                        print(velocities[:20])
    except:
        pass
    
    # Crea un nuovo frame vuoto
    frame = np.zeros((video_height, video_width, 3), dtype=np.uint8)

    # Disegna il cubo sul frame
    cv2.rectangle(frame, p1_square1, p2_square1, (255, 255, 255), -1)
    cv2.rectangle(frame, p1_square2, p2_square2, (255, 255, 255), -1)

    for i in range(len(commands)):
        if commands[i]:
            draw_circle(i)

    # Aggiungi il frame al video
    video.write(frame)

    # Mostra il frame in tempo reale
    cv2.imshow('Video in tempo reale', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):  # Attendere 25 ms per aggiornare il frame, esci se premi 'q'
        break


# Rilascia il video
#video.release()

# Chiudi la finestra di visualizzazione
cv2.destroyAllWindows()
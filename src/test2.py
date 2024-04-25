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
video = cv2.VideoWriter('output.mov', cv2.VideoWriter_fourcc(*'XVID'), 30, (video_width, video_height))

# Carica l'immagine PNG
background_image = cv2.imread('src/images/cielo.png')
giants_image = cv2.imread('src/images/giants.png')
print(giants_image.shape)

commands = [False] * 61
velocities = [0] * 61
colors = [(0, 0, 0)] * 61


def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def draw_circle(command, frame):
    r, g, b = colors[command]
    r = int(r * velocities[command] / 127)
    g = int(g * velocities[command] / 127)
    b = int(b * velocities[command] / 127)
    #cv2.circle(frame, circles[command % 18], circle_ray, (r, g, b), -1)

# Ciclo per generare ogni frame del video
for i in range(60):

    # Leggi input midi se presenti
    try:
        if input.poll():
            received = input.read(10)

            for rec in received:
                if rec[0][0] == 144 or rec[0][0] == 128:
                    commands[rec[0][1] - 36] = not commands[rec[0][1] - 36]
                    if commands[rec[0][1] - 36]:
                        velocities[rec[0][1] - 36] = rec[0][2]
                        colors[rec[0][1] - 36] = get_random_color()
                    print(commands[:20])
                    print(velocities[:20])
    except:
        pass
    
    # Crea un nuovo frame vuoto
    frame = np.zeros((video_height, video_width, 3), dtype=np.uint8)
    #frame = background_image[:video_height][:video_width]
    overlay_h, overlay_w, _ = giants_image.shape
    x_offset = (video_width - overlay_w) // 2
    y_offset = (video_height - overlay_h) // 2
    frame[y_offset:y_offset+overlay_h, x_offset:x_offset+overlay_w] = giants_image[:, :, :3]


    for i in range(len(commands)):
        if commands[i]:
            draw_circle(i, frame)

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
import cv2
import numpy as np
import pygame.midi as midi
import random

# get the MIDI input device
midi.init()
try:
    input = midi.Input(midi.get_default_input_id(), 256)
except:
    pass

# screen dimensions
video_width = 1920
video_height = 1080

# initialize the video
video = cv2.VideoWriter('recordings/output.mov', cv2.VideoWriter_fourcc(*'XVID'), 30, (video_width, video_height))

# load the images
background_image = cv2.imread('src/images/cielo.png')
giants_image = cv2.imread('src/images/giants.png')

# initialize command arrays
commands = [False] * 61
velocities = [0] * 61
colors = [(0, 0, 0)] * 61

def get_random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# loop to generate each frame of the video
for i in range(60):

    # read MIDI input if there is any
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
    
    # create a new empty frame
    frame = np.zeros((video_height, video_width, 3), dtype=np.uint8)

    # overlay an image
    overlay_h, overlay_w, _ = giants_image.shape
    x_offset = (video_width - overlay_w) // 2
    y_offset = (video_height - overlay_h) // 2
    frame[y_offset:y_offset+overlay_h, x_offset:x_offset+overlay_w] = giants_image[:, :, :3]

    # handle commands
    for i in range(len(commands)):
        if commands[i]:
            pass

    # add the frame to the video
    video.write(frame)

    # show the frame in real-time
    cv2.imshow('Video in tempo reale', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):  # wait 25 ms to update the frame, press 'q' to exit
        break

# release the video
video.release()

# close the windows
cv2.destroyAllWindows()
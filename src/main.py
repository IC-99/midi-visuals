import cv2
import numpy as np
from controller import Midi_controller
from visuals import Squares_and_circles, Image_shift

buffer_size = 256

# screen dimensions
video_width = 1920
video_height = 1080

# get the MIDI input device
controller = Midi_controller(buffer_size)

# initialize the video
video = cv2.VideoWriter('recordings/output.mov', cv2.VideoWriter_fourcc(*'XVID'), 30, (video_width, video_height))

# choose the visuals you want to draw
visual = Squares_and_circles(video_width, video_height)
#visual = Image_shift(video_width, video_height)

# loop to generate each frame of the video
while True:

    # read MIDI input if there is any
    controller.read()
    
    # create a new empty frame
    frame = np.zeros((video_height, video_width, 3), dtype=np.uint8)

    visual.draw_background(frame)

    # handle commands
    for i in range(len(controller.commands)):
        if controller.commands[i]:
            visual.draw(frame, [i, controller.velocities[i], controller.colors[i]])

    # add the frame to the video
    video.write(frame)

    # show the frame in real-time
    cv2.imshow('visuals', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):  # wait 25 ms to update the frame, press 'q' to exit
        break

# release the video
video.release()

# close the windows
cv2.destroyAllWindows()
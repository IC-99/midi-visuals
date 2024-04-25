import cv2
import numpy as np
import pygame.midi as midi
import random

class Squares_and_circles:

    def __init__(self, video_width, video_height, square_size = 600, squares_gap = 200, circle_margin = 0.8) -> None:
        self.p1_square1 = (video_width // 2 - squares_gap // 2 - square_size, (video_height - square_size) // 2)
        self.p2_square1 = (self.p1_square1[0] + square_size, self.p1_square1[1] + square_size)
        self.p1_square2 = (video_width // 2 + squares_gap // 2, (video_height - square_size) // 2)
        self.p2_square2 = (self.p1_square2[0] + square_size, self.p1_square2[1] + square_size)
        circle_gap = square_size // 6
        circle_margin = 0.8
        self.circle_ray = int((square_size // 6) * circle_margin)
        p_circle1 = (self.p1_square1[0] + circle_gap, self.p1_square1[1] + circle_gap)
        p_circle2 = (self.p1_square1[0] + circle_gap * 3, self.p1_square1[1] + circle_gap)
        p_circle3 = (self.p1_square1[0] + circle_gap * 5, self.p1_square1[1] + circle_gap)
        p_circle4 = (self.p1_square1[0] + circle_gap, self.p1_square1[1] + circle_gap * 3)
        p_circle5 = (self.p1_square1[0] + circle_gap * 3, self.p1_square1[1] + circle_gap * 3)
        p_circle6 = (self.p1_square1[0] + circle_gap * 5, self.p1_square1[1] + circle_gap * 3)
        p_circle7 = (self.p1_square1[0] + circle_gap, self.p1_square1[1] + circle_gap * 5)
        p_circle8 = (self.p1_square1[0] + circle_gap * 3, self.p1_square1[1] + circle_gap * 5)
        p_circle9 = (self.p1_square1[0] + circle_gap * 5, self.p1_square1[1] + circle_gap * 5)
        p_circle10 = (self.p1_square2[0] + circle_gap, self.p1_square1[1] + circle_gap)
        p_circle11 = (self.p1_square2[0] + circle_gap * 3, self.p1_square1[1] + circle_gap)
        p_circle12 = (self.p1_square2[0] + circle_gap * 5, self.p1_square1[1] + circle_gap)
        p_circle13 = (self.p1_square2[0] + circle_gap, self.p1_square1[1] + circle_gap * 3)
        p_circle14 = (self.p1_square2[0] + circle_gap * 3, self.p1_square1[1] + circle_gap * 3)
        p_circle15 = (self.p1_square2[0] + circle_gap * 5, self.p1_square1[1] + circle_gap * 3)
        p_circle16 = (self.p1_square2[0] + circle_gap, self.p1_square1[1] + circle_gap * 5)
        p_circle17 = (self.p1_square2[0] + circle_gap * 3, self.p1_square1[1] + circle_gap * 5)
        p_circle18 = (self.p1_square2[0] + circle_gap * 5, self.p1_square1[1] + circle_gap * 5)
        # aggregate all the circles in one list
        self.circles = [p_circle1, p_circle2, p_circle3, p_circle4, p_circle5, p_circle6, p_circle7, p_circle8, p_circle9, p_circle10, p_circle11, p_circle12, p_circle13, p_circle14, p_circle15, p_circle16, p_circle17, p_circle18]

    # draw the background image
    def draw_background(self, frame):
        cv2.rectangle(frame, self.p1_square1, self.p2_square1, (255, 255, 255), -1)
        cv2.rectangle(frame, self.p1_square2, self.p2_square2, (255, 255, 255), -1)

    # draw a circle by command
    def draw(self, frame, command, velocity, color):
        r, g, b = color
        r = int(r * velocity / 127)
        g = int(g * velocity / 127)
        b = int(b * velocity / 127)
        cv2.circle(frame, self.circles[command % 18], self.circle_ray, (r, g, b), -1)

class Image_shift:
    def __init__(self, video_width, video_height) -> None:
        self.video_width = video_width
        self.video_height = video_height
        self.background_image = cv2.imread('src/images/giants.png')
        image1 = cv2.imread('src/images/image1.png')
        image2 = cv2.imread('src/images/image2.png')
        image3 = cv2.imread('src/images/image3.png')
        image4 = cv2.imread('src/images/image4.png')
        image5 = cv2.imread('src/images/image5.png')
        self.images = [image1, image2, image3, image4, image5]

    # draw the background image
    def draw_background(self, frame):
        overlay_h, overlay_w, _ = self.background_image.shape
        x_offset = (self.video_width - overlay_w) // 2
        y_offset = (self.video_height - overlay_h) // 2
        frame[y_offset : y_offset + overlay_h, x_offset : x_offset + overlay_w] = self.background_image[:, :, :3]

    # draw an image by command
    def draw(self, frame, command):
        image = self.images[command % len(self.images)]
        overlay_h, overlay_w, _ = image.shape
        x_offset = (self.video_width - overlay_w) // 2
        y_offset = (self.video_height - overlay_h) // 2
        frame[y_offset : y_offset + overlay_h, x_offset : x_offset + overlay_w] = image[:, :, :3]
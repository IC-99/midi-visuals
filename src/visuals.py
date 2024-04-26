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
        self.circle_radius = int((square_size // 6) * circle_margin)
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

    # draw an image by command data (commands, velocities, colors)
    def draw(self, frame, data):
        commands, velocities, colors = data
        for i in range(len(commands)):
            if commands[i]:
                r, g, b = colors[i]
                r = int(r * velocities[i] / 127)
                g = int(g * velocities[i] / 127)
                b = int(b * velocities[i] / 127)
                cv2.circle(frame, self.circles[i % 18], self.circle_radius, (r, g, b), -1)

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

    # draw an image by command data (commands, velocities, colors)
    def draw(self, frame, data):
        commands = data[0]
        for i in range(len(commands)):
            if commands[i]:
                image = self.images[i % len(self.images)]
                overlay_h, overlay_w, _ = image.shape
                x_offset = (self.video_width - overlay_w) // 2
                y_offset = (self.video_height - overlay_h) // 2
                frame[y_offset : y_offset + overlay_h, x_offset : x_offset + overlay_w] = image[:, :, :3]

class Bubble:
    def __init__(self, video_width, video_height, static_radius = 100, max_radius = 500, static_color = (255, 255, 255), decreasing_velocity = 5) -> None:
        self.video_width = video_width
        self.video_height = video_height
        self.static_radius = static_radius
        self.static_color = static_color
        self.radius = static_radius
        self.max_radius = max_radius
        self.center = (video_width // 2, video_height // 2)
        self.decreasing_velocity = decreasing_velocity

    # draw the background image
    def draw_background(self, frame):
        cv2.circle(frame, self.center, self.radius, self.static_color, -1)
        if self.radius > self.static_radius:
            self.radius -= self.decreasing_velocity
            self.radius = max(self.radius, self.static_radius)
                
    # draw an image by command data (commands, velocities, colors)
    def draw(self, frame, data):
        commands = data[0]
        velocities = data[1]
        count = 0
        for i in range(len(commands)):
            if commands[i]:
                count += velocities[i] / 127
        self.radius += int(count * self.decreasing_velocity)
        self.radius = min(self.radius, self.max_radius)

class Bubbles:
    def __init__(self, video_width, video_height, bubbles = [], static_radius = 100, max_radius = 500, static_color = (255, 255, 255), decreasing_velocity = 5) -> None:
        self.video_width = video_width
        self.video_height = video_height
        self.static_radius = static_radius
        self.static_color = static_color
        self.radius = static_radius
        self.max_radius = max_radius
        self.decreasing_velocity = decreasing_velocity
        self.bubbles = bubbles
        if not bubbles:
            p0 = (video_width // 2, video_height // 2)
            p1 = (video_width // 4, video_height // 4)
            p2 = (video_width // 4, (video_height * 3) // 4)
            p3 = ((video_width * 3) // 4, video_height // 4)
            p4 = ((video_width * 3) // 4, (video_height * 3) // 4)
            self.bubbles = [p0, p1, p2, p3, p4]

    # draw the background image
    def draw_background(self, frame):
        for bubble in self.bubbles:
            cv2.circle(frame, bubble, self.radius, self.static_color, -1)
        if self.radius > self.static_radius:
            self.radius -= self.decreasing_velocity
            self.radius = max(self.radius, self.static_radius)
                
    # draw an image by command data (commands, velocities, colors)
    def draw(self, frame, data):
        commands = data[0]
        velocities = data[1]
        count = 0
        for i in range(len(commands)):
            if commands[i]:
                count += velocities[i] / 127
        self.radius += int(count * self.decreasing_velocity)
        self.radius = min(self.radius, self.max_radius)
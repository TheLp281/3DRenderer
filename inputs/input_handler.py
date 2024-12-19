# input_handler.py
import pygame
from pyrr import vector3
from settings import SENSITIVITY
from math import sin,cos,radians
class InputHandler:
    def __init__(self):
        self.last_mouse_pos = None

    def process_input(self, keys):
        movement_input = {
            'w': keys[pygame.K_w],
            's': keys[pygame.K_s],
            'a': keys[pygame.K_a],
            'd': keys[pygame.K_d],
            'shift': keys[pygame.K_LSHIFT],
        }
        return movement_input

    def handle_events(self, yaw, pitch, camera_front):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION:
                yaw, pitch, camera_front = self.handle_mouse_movement(event, yaw, pitch, camera_front)
        return yaw, pitch, camera_front

    def handle_mouse_movement(self, event, yaw, pitch, camera_front):
        if self.last_mouse_pos is None:
            self.last_mouse_pos = pygame.mouse.get_pos()
            return yaw, pitch, camera_front

        x_offset = event.pos[0] - self.last_mouse_pos[0]
        y_offset = event.pos[1] - self.last_mouse_pos[1]
        self.last_mouse_pos = event.pos

        x_offset *= SENSITIVITY
        y_offset *= -SENSITIVITY

        yaw += x_offset
        pitch += y_offset

        pitch = max(min(pitch, 89.0), -89.0)

        yaw %= 360

        front = vector3.Vector3(
            [
                cos(radians(yaw)) * cos(radians(pitch)),
                sin(radians(pitch)),
                sin(radians(yaw)) * cos(radians(pitch)),
            ]
        )
        camera_front = vector3.normalize(front)

        return yaw, pitch, camera_front
input_handler = InputHandler()

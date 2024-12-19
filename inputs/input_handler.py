# input_handler.py
import pygame
import pyrr
from settings import WALK_SPEED, SPRINT_MULTIPLIER, SENSITIVITY, YAW, PITCH
from math import cos, radians, sin

class InputHandler:
    def __init__(self):
        self.last_mouse_pos = None

    def process_input(self, keys, camera_pos, camera_front, camera_up):
        camera_right = pyrr.vector3.normalize(pyrr.vector3.cross(camera_front, camera_up))

        sprint_multiplier = SPRINT_MULTIPLIER if keys[pygame.K_LSHIFT] else 1
        movement_speed = WALK_SPEED * sprint_multiplier
        
        if keys[pygame.K_w]:
            camera_pos += movement_speed * camera_front
        if keys[pygame.K_s]:
            camera_pos -= movement_speed * camera_front
        if keys[pygame.K_a]:
            camera_pos -= movement_speed * camera_right
        if keys[pygame.K_d]:
            camera_pos += movement_speed * camera_right

        front = pyrr.Vector3(
            [
                cos(radians(YAW)) * cos(radians(PITCH)),
                sin(radians(PITCH)),
                sin(radians(YAW)) * cos(radians(PITCH)),
            ]
        )
        camera_front = pyrr.vector.normalize(front)

        return camera_pos, camera_front

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

        front = pyrr.Vector3(
            [
                cos(radians(yaw)) * cos(radians(pitch)),
                sin(radians(pitch)),
                sin(radians(yaw)) * cos(radians(pitch)),
            ]
        )
        camera_front = pyrr.vector.normalize(front)

        return yaw, pitch, camera_front

input_handler = InputHandler()

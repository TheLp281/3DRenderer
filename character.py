# character.py
from pyrr import Vector3, vector3
from math import cos, radians, sin
from settings import WALK_SPEED, SPRINT_MULTIPLIER, YAW, PITCH

class Character:
    def __init__(self, position, camera_up, camera_front):
        self.camera_pos = Vector3(position)  # Ensure position is a Vector3
        self.camera_up = camera_up
        self.camera_front = camera_front

    def update_position(self, movement_input):
        camera_right = vector3.normalize(vector3.cross(self.camera_front, self.camera_up))

        sprint_multiplier = SPRINT_MULTIPLIER if movement_input['shift'] else 1
        movement_speed = WALK_SPEED * sprint_multiplier
        
        if movement_input['w']:
            self.camera_pos += movement_speed * self.camera_front
        if movement_input['s']:
            self.camera_pos -= movement_speed * self.camera_front
        if movement_input['a']:
            self.camera_pos -= movement_speed * camera_right
        if movement_input['d']:
            self.camera_pos += movement_speed * camera_right

    def update_camera(self, yaw, pitch):
        front = Vector3(
            [
                cos(radians(yaw)) * cos(radians(pitch)),
                sin(radians(pitch)),
                sin(radians(yaw)) * cos(radians(pitch)),
            ]
        )
        self.camera_front = vector3.normalize(front)

    def get_camera_pos(self):
        return self.camera_pos

    def get_camera_front(self):
        return self.camera_front

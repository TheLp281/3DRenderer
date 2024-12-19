# main.py
import pygame
import pyrr
from math import *
from settings import YAW,PITCH,W_WIDTH,W_HEIGHT,TEXTURE_FOLDER,FOV,WALK_SPEED,SPRINT_MULTIPLIER,DRAW_DISTANCE,GRID_SIZE,DESIRED_FPS
from game_object import GameObject
from input_handler import input_handler


pygame.init()

pygame.mouse.set_visible(False)
pygame.display.set_caption("3D Renderer")

pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 4)


WHITE = (255, 255, 255)
RED = (255, 0, 0)


last_snap_time = pygame.time.get_ticks()
screen = pygame.display.set_mode(
    (W_WIDTH, W_HEIGHT), pygame.RESIZABLE | pygame.OPENGL | pygame.DOUBLEBUF
)


objects = []


TILE_SPACING = 1

for i in range(GRID_SIZE[0]):
    for j in range(GRID_SIZE[1]):
        position = (i * TILE_SPACING, j * TILE_SPACING, 0.0)
        objects.append(GameObject(position, "brick.jpg", rotation=(90, 0, 0)))

from renderer import *

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
VIEW_LOC = glGetUniformLocation(shader, "view")

camera_pos = pyrr.Vector3([0.0, 0.0, 3.0])
camera_front = pyrr.Vector3([0.0, 0.0, -1.0])
camera_up = pyrr.Vector3([0.0, 1.0, 0.0])





running = True
clock = pygame.time.Clock()

while running:
    keys = pygame.key.get_pressed()
    input_handler.process_input(keys, camera_pos, camera_front, camera_up)


    YAW, PITCH, camera_front = input_handler.handle_events(YAW, PITCH, camera_front)


    glClearColor(0, 0.1, 0.1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    projection = pyrr.matrix44.create_perspective_projection_matrix(
        FOV, W_WIDTH / W_HEIGHT, 0.1, DRAW_DISTANCE
    )
    view = pyrr.matrix44.create_look_at(
        camera_pos, camera_pos + camera_front, camera_up
    )
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(VIEW_LOC, 1, GL_FALSE, view)

    for obj in objects:
        obj.render(model_loc)

    fps = clock.get_fps()
    pygame.display.set_caption(f"FPS: {int(fps)}")

    pygame.draw.rect(screen, RED, (10, 10, 100, 50))
    pygame.display.flip()

    clock.tick(DESIRED_FPS)

pygame.mouse.set_visible(True)

pygame.quit()
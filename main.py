import pygame
from settings import DESIRED_FPS, GRID_SIZE,W_HEIGHT,W_WIDTH
from objects.game_object import GameObject
from inputs.input_handler import input_handler
from graphics.renderer import Renderer

pygame.init()

pygame.mouse.set_visible(False)
pygame.display.set_caption("3D Renderer")

screen = pygame.display.set_mode(
    (W_WIDTH, W_HEIGHT), pygame.RESIZABLE | pygame.OPENGL | pygame.DOUBLEBUF
)

objects = []
TILE_SPACING = 1
for i in range(GRID_SIZE[0]):
    for j in range(GRID_SIZE[1]):
        position = (i * TILE_SPACING, j * TILE_SPACING, 0.0)
        objects.append(GameObject(position, "brick.jpg", rotation=(90, 0, 0)))

renderer = Renderer()

running = True
clock = pygame.time.Clock()

while running:
    keys = pygame.key.get_pressed()
    input_handler.process_input(keys, renderer.camera_pos, renderer.camera_front, renderer.camera_up)
    renderer.handle_input() 

    renderer.render_frame(objects)

    fps = clock.get_fps()
    pygame.display.set_caption(f"FPS: {int(fps)}")
    pygame.display.flip()

    clock.tick(DESIRED_FPS)

pygame.mouse.set_visible(True)
pygame.quit()

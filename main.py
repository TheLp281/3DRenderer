# main.py
import pygame
from settings import DESIRED_FPS, GRID_SIZE, W_HEIGHT, W_WIDTH
from objects.game_object import GameObject
from inputs.input_handler import input_handler
from graphics.renderer import Renderer

class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("3D Renderer")
        self.screen = pygame.display.set_mode(
            (W_WIDTH, W_HEIGHT), pygame.RESIZABLE | pygame.OPENGL | pygame.DOUBLEBUF
        )
        self.objects = []
        self.TILE_SPACING = 1
        self._initialize_objects()
        self.renderer = Renderer()
        self.clock = pygame.time.Clock()

    def _initialize_objects(self):
        for i in range(GRID_SIZE[0]):
            for j in range(GRID_SIZE[1]):
                position = (i * self.TILE_SPACING, j * self.TILE_SPACING, 0.0)
                self.objects.append(GameObject(position, "brick.jpg", rotation=(90, 0, 0)))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        input_handler.process_input(keys, self.renderer.camera_pos, self.renderer.camera_front, self.renderer.camera_up)
        self.renderer.handle_input()

    def render(self):
        self.renderer.render_frame(self.objects)
        fps = self.clock.get_fps()
        pygame.display.set_caption(f"FPS: {int(fps)}")
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.handle_input()
            self.render()
            self.clock.tick(DESIRED_FPS)

        pygame.mouse.set_visible(True)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()

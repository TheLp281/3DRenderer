from OpenGL.GL import *
from os import path
from settings import TEXTURE_FOLDER 
from graphics.texture_loader import load_texture
import numpy as np

class Material:
    def __init__(self, texture_name=None, color=None):
        self.texture_id = glGenTextures(1)
        self.color = color if color else (1.0, 1.0, 1.0) 

        
        if texture_name:
            self.texture_id = glGenTextures(1)
            texture_path = path.join(TEXTURE_FOLDER, texture_name)
            self.texture = load_texture(texture_path, self.texture_id)

            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        else:
            self._create_single_pixel_texture(self.color)

    def _create_single_pixel_texture(self, color):
        color_data = np.array([color[0], color[1], color[2], 1.0], dtype=np.float32)  
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1, 1, 0, GL_RGBA, GL_FLOAT, color_data)
        glBindTexture(GL_TEXTURE_2D, 0)


PREDEFINED_COLORS = [
    (0.8, 0.2, 0.2),  # Red
    (0.2, 0.8, 0.2),  # Green
    (0.2, 0.2, 0.8),  # Blue
    (0.8, 0.8, 0.2),  # Yellow
    (0.8, 0.4, 0.8),  # Purple
    (0.2, 0.8, 0.8),  # Cyan
    (0.8, 0.6, 0.2),  # Orange
]
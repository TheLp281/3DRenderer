from OpenGL.GL import *
import pyrr
import os
import numpy as np
from TextureLoader import load_texture
from settings import TEXTURE_FOLDER

class GameObject:
    def __init__(self, position, texture_name, rotation=np.zeros(3)):
        self.position = position
        self.rotation = np.radians(rotation)
        self.texture_path = os.path.join(TEXTURE_FOLDER, texture_name)
        self.texture_id = glGenTextures(1)
        self.texture = load_texture(self.texture_path, self.texture_id)

        self.translation_matrix = pyrr.matrix44.create_from_translation(pyrr.Vector3(self.position))
        self.rotation_matrix_x = pyrr.matrix44.create_from_x_rotation(self.rotation[0])
        self.rotation_matrix_y = pyrr.matrix44.create_from_y_rotation(self.rotation[1])
        self.rotation_matrix_z = pyrr.matrix44.create_from_z_rotation(self.rotation[2])

    def render(self, model_loc, cube):

        model = self.translation_matrix @ self.rotation_matrix_x @ self.rotation_matrix_y @ self.rotation_matrix_z
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        glDrawElements(GL_TRIANGLES, cube.indices.size, GL_UNSIGNED_INT, None)

    def update_position(self, new_position):

        self.position = new_position
        self.translation_matrix = pyrr.matrix44.create_from_translation(pyrr.Vector3(self.position))

    def update_rotation(self, new_rotation):
        self.rotation = np.radians(new_rotation)
        self.rotation_matrix_x = pyrr.matrix44.create_from_x_rotation(self.rotation[0])
        self.rotation_matrix_y = pyrr.matrix44.create_from_y_rotation(self.rotation[1])
        self.rotation_matrix_z = pyrr.matrix44.create_from_z_rotation(self.rotation[2])


# game_object.py
from OpenGL.GL import *
from graphics.texture_loader import load_texture
from settings import TEXTURE_FOLDER
from objects.cube import cube
from pyrr import matrix44, Vector3
from numpy import zeros, radians
from os import path

class GameObject:
    def __init__(self, position, material, rotation=zeros(3), scale=Vector3([1.0, 1.0, 1.0]), wrap_factor=1):
        self.position = position
        self.rotation = radians(rotation)
        self.scale = scale
        self.wrap_factor = wrap_factor
        self.material = material 

        self.translation_matrix = matrix44.create_from_translation(Vector3(self.position))
        self.rotation_matrix_x = matrix44.create_from_x_rotation(self.rotation[0])
        self.rotation_matrix_y = matrix44.create_from_y_rotation(self.rotation[1])
        self.rotation_matrix_z = matrix44.create_from_z_rotation(self.rotation[2])
        self.scale_matrix = matrix44.create_from_scale(self.scale)

    def render(self, model_loc, shader_program, is_skybox=False):
        model = self.translation_matrix @ self.rotation_matrix_x @ self.rotation_matrix_y @ self.rotation_matrix_z @ self.scale_matrix
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        if is_skybox:
            glUniform1f(glGetUniformLocation(shader_program, "wrap_factor"), self.wrap_factor)

        if self.material.texture_id:
            glBindTexture(GL_TEXTURE_2D, self.material.texture_id)
            glUniform3f(glGetUniformLocation(shader_program, "colorOverride"), 0.0, 0.0, 0.0)  
        else:
            glUniform3f(glGetUniformLocation(shader_program, "colorOverride"), *self.material.color) 
            glUniform1i(glGetUniformLocation(shader_program, "texture1"), 0) 

        glDrawElements(GL_TRIANGLES, cube.indices.size, GL_UNSIGNED_INT, None)

    def update_position(self, new_position):
        self.position = new_position
        self.translation_matrix = matrix44.create_from_translation(Vector3(self.position))

    def update_rotation(self, new_rotation):
        self.rotation = radians(new_rotation)
        self.rotation_matrix_x = matrix44.create_from_x_rotation(self.rotation[0])
        self.rotation_matrix_y = matrix44.create_from_y_rotation(self.rotation[1])
        self.rotation_matrix_z = matrix44.create_from_z_rotation(self.rotation[2])

    def update_scale(self, new_scale):
        self.scale = new_scale
        self.scale_matrix = matrix44.create_from_scale(self.scale) 

    def update_wrap_factor(self, new_wrap_factor):
        self.wrap_factor = new_wrap_factor

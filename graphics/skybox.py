from OpenGL.GL import *
from numpy import array,float32,uint32
from graphics.texture_loader import load_texture


class SkyBox:
    def __init__(self):
        self.faces = ['bottom', 'top', 'left', 'right', 'front', 'back']
        self.skybox_vertices = array([
            -1.0,  1.0, -1.0,
            -1.0, -1.0, -1.0,
            1.0, -1.0, -1.0,
            1.0,  1.0, -1.0,
            -1.0,  1.0,  1.0,
            -1.0, -1.0,  1.0,
            1.0, -1.0,  1.0,
            1.0,  1.0,  1.0,
        ], dtype=float32)

        self.skybox_indices = array([
            0, 1, 2, 0, 2, 3,   
            4, 5, 6, 4, 6, 7,   
            4, 5, 1, 4, 1, 0,   
            3, 2, 6, 3, 6, 7,   
            4, 0, 3, 4, 3, 7,   
            5, 1, 2, 5, 2, 6    
        ], dtype=uint32)

        self._create_skybox()

    def _create_skybox(self):


        self.skybox_VAO = glGenVertexArrays(1)
        glBindVertexArray(self.skybox_VAO)

        self.skybox_VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.skybox_VBO)
        glBufferData(GL_ARRAY_BUFFER, 4 * len(self.skybox_vertices), self.skybox_vertices, GL_STATIC_DRAW)

        self.skybox_EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.skybox_EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * len(self.skybox_indices), self.skybox_indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))

        self.skybox_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.skybox_texture)

        self.update_skybox_faces()

        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)


    def update_skybox_faces(self):
        for i, face in enumerate(self.faces):
            load_texture(f"{face}.png", i)
    
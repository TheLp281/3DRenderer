# renderer.py
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from settings import *
from objects.cube import Cube
from graphics.shaders import vertex_shader, fragment_shader
from pyrr import matrix44,Vector3
from inputs.input_handler import input_handler  

class Renderer:
    def __init__(self):
        self.shader = compileProgram(
            compileShader(vertex_shader, GL_VERTEX_SHADER),
            compileShader(fragment_shader, GL_FRAGMENT_SHADER),
        )
        self._setup_opengl()
        self._create_cube()

        self.camera_pos = Vector3([0.0, 0.0, 3.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])

        self.YAW = -90.0  
        self.PITCH = 0.0 

    def _setup_opengl(self):
        glUseProgram(self.shader)

        light_position = [-1.0, 2.0, -2.0]
        light_ambient = [0.2, 0.2, 0.2]
        light_diffuse = [0.5, 0.5, 0.5]
        light_specular = [1.0, 1.0, 1.0]
        view_position = [0.0, 5.0, 1.0]
        shininess = 1

        glUniform3fv(glGetUniformLocation(self.shader, "light.position"), 1, light_position)
        glUniform3fv(glGetUniformLocation(self.shader, "light.ambient"), 1, light_ambient)
        glUniform3fv(glGetUniformLocation(self.shader, "light.diffuse"), 1, light_diffuse)
        glUniform3fv(glGetUniformLocation(self.shader, "light.specular"), 1, light_specular)
        glUniform3fv(glGetUniformLocation(self.shader, "viewPos"), 1, view_position)
        glUniform1f(glGetUniformLocation(self.shader, "shininess"), shininess)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def _create_cube(self):
        self.cube = Cube()
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, self.cube.vertices.nbytes, self.cube.vertices, GL_STATIC_DRAW)

        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.cube.indices.nbytes, self.cube.indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.cube.vertices.itemsize * 5, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.cube.vertices.itemsize * 5, ctypes.c_void_p(12))

    def handle_input(self):
        self.YAW, self.PITCH, self.camera_front = input_handler.handle_events(self.YAW, self.PITCH, self.camera_front)

    def render_frame(self, objects):
        glClearColor(0, 0.1, 0.1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        projection = matrix44.create_perspective_projection_matrix(
            FOV, W_WIDTH / W_HEIGHT, 0.1, DRAW_DISTANCE
        )
        view = matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

        glUniformMatrix4fv(glGetUniformLocation(self.shader, "projection"), 1, GL_FALSE, projection)
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "view"), 1, GL_FALSE, view)

        for obj in objects:
            obj.render(glGetUniformLocation(self.shader, "model"), self.shader)

from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from graphics.shaders import vertex_shader, fragment_shader, skybox_vertex_shader, skybox_fragment_shader
from pyrr import matrix44, Vector3
from objects.cube import Cube
from settings import *
from graphics.skybox import SkyBox
class Renderer:
    def __init__(self,input_handler):
        self.shader = compileProgram(
            compileShader(vertex_shader, GL_VERTEX_SHADER),
            compileShader(fragment_shader, GL_FRAGMENT_SHADER),
        )
        self.skybox_shader = compileProgram(
            compileShader(skybox_vertex_shader, GL_VERTEX_SHADER),
            compileShader(skybox_fragment_shader, GL_FRAGMENT_SHADER),
        )

        self._setup_opengl()
        self._create_cube()
        self.skybox = SkyBox()


        self.camera_pos = Vector3(START_POSITION)
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        
        self.YAW = 90
        self.PITCH = 0.0

        self.input_handler = input_handler

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
        self.YAW, self.PITCH, self.camera_front = self.input_handler.handle_events(self.YAW, self.PITCH, self.camera_front)



    def render_skybox(self, projection, view):
        glDepthMask(GL_FALSE)  
        
        glUseProgram(self.skybox_shader)
        glUniformMatrix4fv(glGetUniformLocation(self.skybox_shader, "projection"), 1, GL_FALSE, projection)
        
        view = matrix44.create_look_at(
            self.camera_pos,  
            self.camera_pos + self.camera_front,  
            self.camera_up  
        )
        view[3][0] = 0
        view[3][1] = 0
        view[3][2] = 0

        glUniformMatrix4fv(glGetUniformLocation(self.skybox_shader, "view"), 1, GL_FALSE, view)

        glBindVertexArray(self.skybox.skybox_VAO)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.skybox.skybox_texture)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_INT, None)

        glDepthMask(GL_TRUE)  


    def render_frame(self, objects):
        glClearColor(0, 0.1, 0.1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        projection = matrix44.create_perspective_projection_matrix(
            FOV, W_WIDTH / W_HEIGHT, 0.1, DRAW_DISTANCE
        )
        self.render_skybox(projection, None)

        glUseProgram(self.shader)

        projection_location = glGetUniformLocation(self.shader, "projection")
        if projection_location == -1:
            print("Uniform 'projection' not found!")
        else:
            glUniformMatrix4fv(projection_location, 1, GL_FALSE, projection)

        view = matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

        view_location = glGetUniformLocation(self.shader, "view")
        if view_location == -1:
            print("Uniform 'view' not found!")
        else:
            glUniformMatrix4fv(view_location, 1, GL_FALSE, view)

        for obj in objects:
            obj.render(glGetUniformLocation(self.shader, "model"), self.shader)

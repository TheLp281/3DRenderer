# shaders.py

vertex_shader = """
#version 330 core
layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texCoord;
uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
out vec2 fragTexCoord;
void main()
{
    gl_Position = projection * view * model * vec4(position, 1.0);
    fragTexCoord = texCoord;
}
"""

fragment_shader = """
#version 330 core
in vec2 fragTexCoord;
out vec4 color;
uniform sampler2D texture1;
uniform float wrap_factor;

void main()
{
    vec2 tiled_coords = fragTexCoord * wrap_factor;
    color = texture(texture1, tiled_coords);
}
"""
skybox_vertex_shader = """
#version 330 core
layout(location = 0) in vec3 position;
uniform mat4 projection;
uniform mat4 view;
out vec3 TexCoords;
void main()
{
    gl_Position = projection * view * vec4(position, 1.0);
    TexCoords = position;
}
"""

skybox_fragment_shader = """
#version 330 core
in vec3 TexCoords;
out vec4 color;
uniform samplerCube skybox;
void main()
{
    color = texture(skybox, TexCoords);
}
"""

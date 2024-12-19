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
void main()
{
    color = texture(texture1, fragTexCoord);
}
"""

#version 330

uniform mat4 view;
uniform mat4 perspective;
in vec3 position;

void main() {
    gl_Position = perspective * view * vec4(position, 1.0);
    //gl_Position = vec4(position, 1.0);
}
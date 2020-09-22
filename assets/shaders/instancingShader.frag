#version 130

uniform sampler2D p3d_Texture0;

// Input from vertex shader
in vec2 texcoord;

out vec4 outputColor;

void main() {
  vec4 color = texture(p3d_Texture0, texcoord);
  outputColor = vec4(1, 0, 0, 0.5);
}
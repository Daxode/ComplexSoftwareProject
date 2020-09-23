#version 130

uniform sampler2D p3d_Texture0;

// Input from vertex shader
in vec2 texcoord;
in vec3 normal;
in float value;

out vec4 outputColor;

void main() {
  vec4 color = texture(p3d_Texture0, texcoord);
  vec3 rgb_normal = normal * 0.5 + 0.5;

  outputColor = vec4(mod(rgb_normal.x*8, 2)*0.5, rgb_normal.yz, 0.5)*value;
}
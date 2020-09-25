#version 130

//#pragma include "../utils/p3d_light_sources"

#define MAX_ITERATION 20

uniform sampler2D p3d_Texture0;

// Input from vertex shader
in vec2 texcoord;
in vec3 normal;

out vec4 outputColor;

void main() {
  vec4 color = texture(p3d_Texture0, texcoord);
  vec3 rgb_normal = (normalize(normal) + 1) * 0.5;

//  outputColor = saturate(dot(normal, p3d_LightSource[0]));
  outputColor = vec4(rgb_normal, 1);
}
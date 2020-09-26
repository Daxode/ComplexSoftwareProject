#version 130

#pragma include "../utils/p3d_light_sources.frag"

#define MAX_ITERATION 20

uniform sampler2D p3d_Texture0;

// Input from vertex shader
in vec2 texcoord;
in vec3 vertexNormal;
in vec3 primNormal;

out vec4 outputColor;

void main() {
  vec4 color = texture(p3d_Texture0, texcoord);
  vec3 rgb_normal = (normalize(primNormal) + 1) * 0.5;

  //outputColor = vec4(rgb_normal, 1)*clamp(vec4(dot(primNormal, p3d_LightSource[0].position.xyz)),0,1);
  outputColor = vec4(rgb_normal, 1);//*clamp(primNormal, 0, 1).x;
  //outputColor = vec4(rgb_normal, 1);
}
#version 130

#pragma include "../utils/p3d_light_sources.glsl"

#define MAX_ITERATION 20

uniform sampler2D p3d_Texture0;

// Input from vertex shader
in vec2 texcoord;
in vec3 normal;
in vec3 viewspacePos;

out vec4 outputColor;

void main() {
  //vec4 color = texture(p3d_Texture0, texcoord);
  vec3 rgb_normal = (normalize(normal) + 1) * 0.5;

  vec3 lightDir = p3d_LightSource[0].position.xyz;
  if (p3d_LightSource[0].position.w != 0) lightDir -= viewspacePos;
  lightDir = normalize(-lightDir);

  float lambertian = (dot(lightDir, normal)+1)*0.5;
  lambertian = texture(p3d_Texture0, vec2(lambertian, 0.5)).x;

  outputColor = vec4(lambertian)*vec4(1, 0.5, 0.5, 1)+vec4(0.1,0.05,0.05,1);
}
#version 130

#pragma include "../utils/p3d_light_sources.frag"

#define MAX_ITERATION 20

uniform sampler2D p3d_Texture0;
uniform mat4 p3d_ViewMatrixInverse;

uniform struct {
  vec4 ambient;
} p3d_LightModel;

// Input from vertex shader
in vec2 texcoord;
in vec3 vertexNormal;
in vec3 primNormal;

out vec4 outputColor;
const float atten = 1.0;
const float shininess = 0.5;
const vec3 specColor = vec3(1);
const vec3 matColor = vec3(0,1,0);

void main() {
  vec4 color = texture(p3d_Texture0, texcoord);
  vec3 rgb_normal = (normalize(primNormal) + 1) * 0.5;

  vec3 cam_pos = p3d_ViewMatrixInverse[3].xyz;
  vec3 cam_dir = -p3d_ViewMatrixInverse[2].xyz;

  //outputColor = vec4(rgb_normal, 1)*clamp(vec4(dot(primNormal, )),0,1);
  //outputColor = vec4(rgb_normal, 1);//*clamp(primNormal, 0, 1).x;
  vec3 lightDir = p3d_LightSource[0].position.xyz;
  lightDir = vec3(0.5);
  outputColor = vec4(rgb_normal, 1)*clamp(dot(vertexNormal, lightDir)+0.1*dot(p3d_LightModel.ambient.xyz, vec3(1)),0,1);


  //vec3 diffuseReflection = atten * p3d_LightSource[0].color.xyz * max(primNormal, lightDir);

  //vec3 lightReflectDir = reflect(-lightDir, primNormal);
  //float lightSeeDir = max(0.0, dot(lightReflectDir, cam_dir));
  //vec3 shininessPower = vec3(pow(lightSeeDir.x, shininess), pow(lightSeeDir.y, shininess), pow(lightSeeDir.z, shininess));

  //float shininessPower = pow(lightSeeDir, (shininess));

  //vec3 specularReflect = atten * specColor * shininessPower;

  //outputColor = vec4(matColor*(diffuseReflection+p3d_LightModel.ambient.xyz), 1);
}
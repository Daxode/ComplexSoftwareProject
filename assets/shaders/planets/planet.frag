#version 130

#pragma include "../utils/p3d_light_sources.glsl"

#define MAX_ITERATION 20

// Input from vertex shader
in vec2 texcoord;
in vec3 vertexNormal;
in vec3 primNormal;
in vec3 FragPos;
in float num;

in vec3 pospos;

in vec3 cam_pos;
in vec3 cam_dir;

out vec4 outputColor;
const float atten = 0.5;
const float shininess = 0.5;

const float specularStrength = 0.9;
const vec3 specColor = vec3(1,1,1);
const vec3 matColor = vec3(0,0.2,0);

vec3 remap(vec3 iMin, vec3 iMax, vec3 oMin, vec3 oMax, vec3 v) {
  vec3 t = smoothstep(iMin, iMax, v);
  return mix(oMin, oMax, t);
}

float remap(float iMin, float iMax, float oMin, float oMax, float v) {
  float t = smoothstep(iMin, iMax, v);
  return mix(oMin, oMax, t);
}

void main() {
  vec3 rgb_normal = (normalize(primNormal) + 0.5) * 0.5;

  //outputColor = vec4(rgb_normal, 1)*clamp(vec4(dot(primNormal, )),0,1);
  //outputColor = vec4(rgb_normal, 1);//*clamp(primNormal, 0, 1).x;
  vec3 lightDir = p3d_LightSource[0].position.xyz;
  lightDir = vec3(0,-0.5,0.5);

  float diff = max(dot(primNormal, lightDir), 0.0);
  vec3 diffuse = diff * vec3(0.1);//p3d_LightSource[0].color.xyz;

  vec3 viewDir = normalize(cam_pos - FragPos);
  vec3 reflectDir = reflect(lightDir, normalize(primNormal));

  float spec = pow(max(dot(-viewDir, reflectDir), 0.0), 32);
  vec3 specular = specularStrength * spec * specColor;

  vec3 light = diffuse + specular;
  //if (any(lessThan(normalize(pospos), vec3(0)))) light = vec3(0);

  vec3 result = (p3d_LightModel.ambient.xyz+light) * vec3(remap(0.5, 10, 0, 1, dot(pospos,vec3(1))));
  outputColor = vec4(result, 1);

  //outputColor = vec4()
  //outputColor = vec4(rgb_normal, 1);// * smoothstep(0,1, dot(vertexNormal, lightDir)+0.9*dot(p3d_LightModel.ambient.xyz, vec3(1)));
//  vec3 diffuseReflection = atten * p3d_LightSource[0].color.xyz * max(normalize(primNormal), lightDir);
//  vec3 lightReflectDir = reflect(-lightDir, normalize(primNormal));
//  float lightSeeDir = max(0.0, dot(lightReflectDir, cam_dir));
//  vec3 shininessPower = vec3(pow(lightSeeDir.x, shininess), pow(lightSeeDir.y, shininess), pow(lightSeeDir.z, shininess));
//  float shininessPower = pow(lightSeeDir, (shininess));
//  vec3 specularReflect = atten * specColor * shininessPower;
//
//  outputColor = vec4(matColor*(diffuseReflection+p3d_LightModel.ambient.xyz), 1);
}
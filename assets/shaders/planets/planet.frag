#version 130

#pragma include "../utils/p3d_light_sources.glsl"
#pragma include "../utils/p3d_material.glsl"

// Input from vertex shader
in vec3 viewspacePos;
in vec4 fragPos;
in vec3 vertexNormal;
in vec3 primNormal;
in float num;

in vec3 diffuseColor;
in float specStrength;

in vec3 cam_pos;
in vec3 cam_dir;

out vec4 outputColor;

vec3 remap(vec3 iMin, vec3 iMax, vec3 oMin, vec3 oMax, vec3 v) {
  vec3 t = smoothstep(iMin, iMax, v);
  return mix(oMin, oMax, t);
}

float remap(float iMin, float iMax, float oMin, float oMax, float v) {
  float t = smoothstep(iMin, iMax, v);
  return mix(oMin, oMax, t);
}

void main() {
  vec3 illumLightSum = vec3(0);
  vec3 normal = normalize(primNormal);

  //diffuseColor = p3d_Material.diffuse.xyz;
  //specStrength = p3d_Material.specular.x;

  for (int i = 0; i < p3d_LightSource.length; i++) {
    vec3 lightDir = p3d_LightSource[i].position.xyz;
    if (p3d_LightSource[i].position.w != 0) lightDir -= viewspacePos;

    float distance = length(lightDir);
    distance = distance * distance;
    lightDir = normalize(lightDir);

    float lambertian = max(dot(lightDir, normal), 0.0);
    float specular = 0.0;

    if (lambertian > 0.0) {
      vec3 viewDir = normalize(-viewspacePos);

      // this is blinn phong
      vec3 halfDir = normalize(lightDir + viewDir);
      float specAngle = max(dot(halfDir, normal), 0.0);
      specular = pow(specAngle, p3d_Material.shininess);
    }
    vec3 illumDiffuse = diffuseColor * lambertian * p3d_LightSource[i].color.xyz * 1 / distance;
    vec3 illumSpecular = diffuseColor * specStrength * specular * p3d_LightSource[i].color.xyz * 1 / distance;

    illumLightSum += illumDiffuse+illumSpecular;
  }

  vec3 colorGammaCorrected = pow(p3d_LightModel.ambient.xyz*diffuseColor+illumLightSum, vec3(0.49504950495));
  // use the gamma corrected color in the fragment0
  outputColor = vec4(colorGammaCorrected, 1.0);
}
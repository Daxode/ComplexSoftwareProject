#version 130

#pragma include "../utils/p3d_light_sources.glsl"
#pragma include "../utils/p3d_material.glsl"

// Input from vertex shader
in vec3 viewspacePos;
in vec4 fragPos;
in vec3 vertexNormal;
in vec3 primNormal;
in float num;

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
  int mode = 1;
  //vec3 viewDir = normalize(viewspacePos.xyz-cam_pos);
  vec3 illumLightSum = vec3(0);
  vec3 normal = normalize(primNormal);

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

      // this is phong (for comparison)
      if (mode == 2) {
        vec3 reflectDir = reflect(-lightDir, normal);
        specAngle = max(dot(reflectDir, viewDir), 0.0);
        // note that the exponent is different here
        specular = pow(specAngle, p3d_Material.shininess/4.0);
      }
    }
    vec3 illumDiffuse = (p3d_Material.diffuse.xyz) * lambertian * p3d_LightSource[i].color.xyz * 1 / distance;
    vec3 illumSpecular = p3d_Material.diffuse.xyz*p3d_Material.specular * specular * p3d_LightSource[i].color.xyz * 1 / distance;

    illumLightSum += illumDiffuse+illumSpecular;
  }

  //vec3 reflectDir = reflect(-lightDir, normalize(primNormal));
  //float spec = pow(max(dot(viewDir, reflectDir), 0.0), 64);
  //vec3 specular = specularStrength * spec * specColor;

  vec3 colorGammaCorrected = pow(p3d_LightModel.ambient.xyz*p3d_Material.ambient.xyz+illumLightSum, vec3(0.49504950495));
  // use the gamma corrected color in the fragment0
  outputColor = vec4(colorGammaCorrected, 1.0);
}
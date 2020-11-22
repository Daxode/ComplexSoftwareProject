#version 130

#pragma include "../utils/p3d_light_sources.glsl"
#pragma include "../utils/p3d_material.glsl"

uniform sampler2D p3d_Texture1;

// Input from vertex shader
in vec3 viewspacePos;
in vec3 vertexNormal;
in vec3 primNormal;
in float num;

in vec3 diffuseColor;
in float specStrength;

in vec3 cam_pos;
//in vec3 cam_dir;

in vec4[4] shadow_uv;

out vec4 outputColor;

vec3 remap(vec3 iMin, vec3 iMax, vec3 oMin, vec3 oMax, vec3 v) {
  vec3 t = smoothstep(iMin, iMax, v);
  return mix(oMin, oMax, t);
}

float remap(float iMin, float iMax, float oMin, float oMax, float v) {
  float t = smoothstep(iMin, iMax, v);
  return mix(oMin, oMax, t);
}


float textureProjSoft(sampler2DShadow tex, vec4 uv, float bias, float blur) {
  float result = textureProj(tex, uv, bias);
  result += textureProj(tex, vec4(uv.xy + vec2( -0.326212, -0.405805)*blur, uv.z-bias, uv.w));
  result += textureProj(tex, vec4(uv.xy + vec2(-0.840144, -0.073580)*blur, uv.z-bias, uv.w));
  result += textureProj(tex, vec4(uv.xy + vec2(-0.695914, 0.457137)*blur, uv.z-bias, uv.w));
  result += textureProj(tex, vec4(uv.xy + vec2(-0.203345, 0.620716)*blur, uv.z-bias, uv.w));
  result += textureProj(tex, vec4(uv.xy + vec2(0.962340, -0.194983)*blur, uv.z-bias, uv.w));
  result += textureProj(tex, vec4(uv.xy + vec2(0.473434, -0.480026)*blur, uv.z-bias, uv.w));
  result += textureProj(tex, vec4(uv.xy + vec2(0.519456, 0.767022)*blur, uv.z-bias, uv.w));
  result += textureProj(tex, vec4(uv.xy + vec2(0.185461, -0.893124)*blur, uv.z-bias, uv.w));
  result += textureProj(tex, vec4(uv.xy + vec2(0.507431, 0.064425)*blur, uv.z-bias, uv.w));
  result += textureProj(tex, vec4(uv.xy + vec2(0.896420, 0.412458)*blur, uv.z-bias, uv.w));
  result += textureProj(tex, vec4(uv.xy + vec2(-0.321940, -0.932615)*blur, uv.z-bias, uv.w));
  result += textureProj(tex, vec4(uv.xy + vec2(-0.791559, -0.597705)*blur, uv.z-bias, uv.w));
  return result/13.0;
}



void main() {
  vec3 illumLightSum = vec3(0);
  vec3 normal = normalize(primNormal);

  for (int i = 0; i < p3d_LightSource.length(); i++) {
    float shadowScale = 1;
    shadowScale = textureProj(p3d_LightSource[i].shadowMap, shadow_uv[i]);
    //shadowScale = textureProjSoft(p3d_LightSource[i].shadowMap, shadow_uv[i], 0.0001, 0.001);
    vec3 lightDir = p3d_LightSource[i].position.xyz;
    if (p3d_LightSource[i].position.w != 0) {
      lightDir -= viewspacePos;
    }

    float distance = length(lightDir);
    distance = distance * distance;
    lightDir = normalize(-lightDir);

    float lambertian = max(dot(lightDir, normal), 0.0);
    //lambertian = texture(p3d_Texture1, vec2(lambertian, 0.5)).x; // --Adds diffuse toon shading

    float specular = 0.0;

    if (lambertian > 0.0) {
      vec3 viewDir = normalize(-viewspacePos);

      // this is blinn phong
      vec3 halfDir = normalize(lightDir + viewDir);
      float specAngle = max(dot(halfDir, normal), 0.0);
      specular = pow(specAngle, p3d_Material.shininess);
      //specular = texture(p3d_Texture1, vec2(specular, 0.5)).x; // --Adds specular toon shading
    }
    vec3 illumDiffuse = diffuseColor *                 lambertian * p3d_LightSource[i].color.xyz / (distance);
    vec3 illumSpecular = diffuseColor * specStrength * specular   * p3d_LightSource[i].color.xyz / (distance);
    illumLightSum += (illumDiffuse+illumSpecular)*shadowScale;
  }

  vec3 colorGammaCorrected = pow(p3d_LightModel.ambient.xyz*diffuseColor+illumLightSum, vec3(0.49504950495));
  //colorGammaCorrected = texture(p3d_Texture1, vec2(length(colorGammaCorrected.xyz), 0.5), 0).x*colorGammaCorrected; // - Adds brightness toon shading

  // use the gamma corrected color in the fragment0
  outputColor = vec4(colorGammaCorrected, 1);
}
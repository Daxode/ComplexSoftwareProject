#version 430

#pragma include "../utils/p3d_light_sources.glsl"

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ViewMatrixInverse;
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat3 p3d_NormalMatrix;

uniform sampler2D p3d_Texture0;

layout(rgba32f) uniform readonly image3D vertexBufferEdge;
layout(rgba32i) uniform readonly iimageBuffer triangleBuffer;
layout(rgba32f) uniform readonly imageBuffer normalBuffer;

//Inputs
in vec2 p3d_MultiTexCoord0;

// Output to fragment shader
out vec2 texcoord;
out vec3 vertexNormal;
out vec3 primNormal;
out float num;
out vec4 fragPos;
out vec3 viewspacePos;

out vec3 diffuseColor;
out float specStrength;

out vec3 cam_pos;
out vec3 cam_dir;
out vec4[4] shadow_uv;

void main() {
  ivec3 vertexIndex = imageLoad(triangleBuffer, gl_VertexID).xyz;
  vec4 vertex = vec4(imageLoad(vertexBufferEdge, vertexIndex).xyz, 1);
  gl_Position = p3d_ModelViewProjectionMatrix*vertex;
  fragPos = gl_Position;

  vec4 viewspacePos4 = p3d_ModelViewMatrix * vertex;
  viewspacePos = vec3(viewspacePos4) / viewspacePos4.w;

  vec4 primNormalWVal = imageLoad(normalBuffer, int(gl_VertexID/3));
  primNormal = primNormalWVal.xyz;
  primNormal = p3d_NormalMatrix * primNormal;

  vertexNormal = normalize(vertex.xyz);

  texcoord = p3d_MultiTexCoord0;
  num = primNormalWVal.w;

  vec4 getColor = texelFetch(p3d_Texture0, ivec2(8-num, 8-num), 0);
  diffuseColor = getColor.xyz;
  diffuseColor = diffuseColor*diffuseColor;
  specStrength = getColor.w;

  cam_pos = p3d_ViewMatrixInverse[3].xyz;
  cam_dir = -p3d_ViewMatrixInverse[2].xyz;

  for (int i = 0; i < p3d_LightSource.length; i++) {
    shadow_uv[i] = p3d_LightSource[i].shadowViewMatrix * (p3d_ModelViewMatrix * vertex);
  }
}
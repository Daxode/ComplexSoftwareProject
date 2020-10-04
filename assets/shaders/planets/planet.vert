#version 430

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ViewMatrixInverse;
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat3 p3d_NormalMatrix;

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

out vec3 cam_pos;
out vec3 cam_dir;

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

  cam_pos = p3d_ViewMatrixInverse[3].xyz;
  cam_dir = -p3d_ViewMatrixInverse[2].xyz;
}
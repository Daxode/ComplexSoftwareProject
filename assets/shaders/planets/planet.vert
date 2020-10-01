#version 430

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ViewMatrixInverse;

layout(rgba32f) uniform readonly image3D vertexBufferEdge;
layout(rgba32i) uniform readonly iimageBuffer triangleBuffer;
layout(rgba32f) uniform readonly imageBuffer normalBuffer;

// Vertex inputs
in vec2 p3d_MultiTexCoord0;
in vec3 p3d_Normal;

// Output to fragment shader
out vec2 texcoord;
out vec3 vertexNormal;
out vec3 primNormal;
out vec3 FragPos;
out float num;
out vec3 pospos;

out vec3 cam_pos;
out vec3 cam_dir;

void main() {
  ivec3 vertexIndex = imageLoad(triangleBuffer, gl_VertexID).xyz;
  vec4 vertex = vec4(imageLoad(vertexBufferEdge, vertexIndex).xyz, 1);
  //vertex = vec4(gl_VertexID, gl_VertexID, gl_VertexID+1, 0);
  gl_Position = p3d_ModelViewProjectionMatrix*vertex;
  vec4 primNormalWVal = imageLoad(normalBuffer, int(gl_VertexID/3));
  primNormal = primNormalWVal.xyz;
  primNormal = mat3(transpose(inverse(p3d_ModelMatrix))) * primNormal;
  vertexNormal = normalize(vertex.xyz);
  FragPos = vec3(p3d_ModelViewProjectionMatrix * vertex);
  texcoord = p3d_MultiTexCoord0;
  num = primNormalWVal.w;
  pospos = vertex.xyz;

  cam_pos = p3d_ViewMatrixInverse[3].xyz;
  cam_dir = -p3d_ViewMatrixInverse[2].xyz;
}
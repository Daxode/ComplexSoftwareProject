#version 430

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
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

void main() {
  ivec3 vertexIndex = imageLoad(triangleBuffer, gl_VertexID).xyz;
  vec4 vertex = vec4(imageLoad(vertexBufferEdge, vertexIndex).xyz, 1);
  //vertex = vec4(gl_VertexID, gl_VertexID, gl_VertexID+1, 0);
  gl_Position = p3d_ModelViewProjectionMatrix*vertex;
  vec4 primNormalWVal = imageLoad(normalBuffer, int(gl_VertexID/3));
  primNormal = primNormalWVal.xyz;
  primNormal = mat3(transpose(inverse(p3d_ModelMatrix))) * primNormal;
  vertexNormal = normalize(vertex.xyz);
  FragPos = vec3(p3d_ModelMatrix * gl_Position);
  texcoord = p3d_MultiTexCoord0;
  num = primNormalWVal.w;
}
#version 430

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
layout(rgba32f) uniform readonly image3D vertexBufferEdge;
layout(rgba32i) uniform readonly iimageBuffer triangleBuffer;

// Vertex inputs
in vec2 p3d_MultiTexCoord0;
in vec3 p3d_Normal;

// Output to fragment shader
out vec2 texcoord;
out vec3 normal;

void main() {
  ivec3 vertexIndex = imageLoad(triangleBuffer, gl_VertexID).xyz;
  vec4 vertex = imageLoad(vertexBufferEdge, vertexIndex);
  gl_Position = p3d_ModelViewProjectionMatrix*vertex;
  normal = p3d_Normal;
  texcoord = p3d_MultiTexCoord0;
}
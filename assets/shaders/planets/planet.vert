#version 430

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ViewProjectionMatrix;
layout(rgba32f) uniform readonly image3D vertexBufferEdge;
layout(rgba32i) uniform readonly iimageBuffer triangleBuffer;
layout(rgba32f) uniform readonly imageBuffer normalBuffer;

// Vertex inputs
in vec2 p3d_MultiTexCoord0;
in vec3 p3d_Normal;

// Output to fragment shader
out vec2 texcoord;
out vec3 normal;

void main() {
  ivec3 vertexIndex = imageLoad(triangleBuffer, gl_VertexID).xyz;
  vec4 vertex = vec4(imageLoad(vertexBufferEdge, vertexIndex).xyz, 1);
  //vertex = vec4(gl_VertexID, gl_VertexID, gl_VertexID+1, 0);
  gl_Position = p3d_ModelViewProjectionMatrix*vertex;
  normal = imageLoad(normalBuffer, int(gl_VertexID/3)).xyz;
  texcoord = p3d_MultiTexCoord0;
}
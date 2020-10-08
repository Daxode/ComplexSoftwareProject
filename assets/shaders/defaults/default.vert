#version 140

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
in vec3 p3d_Normal;

// Output to fragment shader
out vec2 texcoord;
out vec3 normal;
out vec3 viewspacePos;

void main() {
  gl_Position = p3d_ModelViewProjectionMatrix*p3d_Vertex;

  vec4 viewspacePos4 = p3d_ModelViewMatrix * p3d_Vertex;
  viewspacePos = vec3(viewspacePos4) / viewspacePos4.w;

  normal = p3d_Normal;

  texcoord = p3d_MultiTexCoord0;
}
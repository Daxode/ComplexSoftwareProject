#version 140

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform samplerBuffer InstancingData;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
in vec3 p3d_Normal;


// Output to fragment shader
out vec2 texcoord;
out vec3 normal;

void main() {
  vec4 locationOffset = texelFetch(InstancingData, gl_InstanceID);
  gl_Position = p3d_ModelViewProjectionMatrix*(locationOffset + p3d_Vertex);
  normal = p3d_Normal;
  texcoord = p3d_MultiTexCoord0;
}
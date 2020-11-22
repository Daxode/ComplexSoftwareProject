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
  int data_index = gl_InstanceID * 4;

  vec4 data_0 = texelFetch(InstancingData, data_index);
  vec4 data_1 = texelFetch(InstancingData, data_index + 1);
  vec4 data_2 = texelFetch(InstancingData, data_index + 2);
  vec4 data_3 = texelFetch(InstancingData, data_index + 3);

  mat4 transform_mat = mat4(data_0, data_1, data_2, data_3);

  gl_Position = (p3d_ModelViewProjectionMatrix*transform_mat*p3d_Vertex);

  normal = mat3(transform_mat) * p3d_Normal;

  texcoord = p3d_MultiTexCoord0;
}
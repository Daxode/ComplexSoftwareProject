#version 140

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform samplerBuffer InstancingData;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

// Output to fragment shader
out vec2 texcoord;

void main() {
  int data_index = gl_InstanceID * 4;

  vec4 data_0 = texelFetch(InstancingData, data_index);
  vec4 data_1 = texelFetch(InstancingData, data_index + 1);
  vec4 data_2 = texelFetch(InstancingData, data_index + 2);
  vec4 data_3 = texelFetch(InstancingData, data_index + 3);

  mat4 transform_mat = mat4(data_0, data_1, data_2, data_3);

  vec3 outputVec = (transform_mat * p3d_Vertex).xyz;
  // Also transform normal, not 100% correct but works out nicely
  // vOutput.normal = mat3(transform_mat) * vOutput.normal;

  gl_Position = p3d_ModelViewProjectionMatrix * vec4(outputVec, 1);

  texcoord = p3d_MultiTexCoord0;
}
#version 430

#pragma include "../../external_libs/glsl-noise/simplex/three_d.glsl"

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
layout(rgba32f, binding = 0) uniform readonly image3D InstancingData;
uniform ivec3 size;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
in vec3 p3d_Normal;

// Output to fragment shader
out vec2 texcoord;
out vec3 normal;
out float value;

void main() {

  ivec3 texelCoords = ivec3(gl_InstanceID % size.x, (gl_InstanceID / size.x)%size.y, gl_InstanceID / (size.x*size.y));

  vec4 locationOffset = imageLoad(InstancingData, texelCoords);
//  if (locationOffset.w < 0.5) {
//    return;
//  }

  gl_Position = p3d_ModelViewProjectionMatrix*(vec4(locationOffset.xyz + p3d_Vertex.xyz, 1));
  value = locationOffset.w;
  normal = p3d_Normal;
  texcoord = p3d_MultiTexCoord0;
}
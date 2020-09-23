#version 430

#pragma include "../../external_libs/glsl-noise/simplex/three_d.glsl"

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform int gridSize;
layout(rgba32f, binding = 0) uniform readonly image3D InstancingData;
uniform vec3 mouseTime;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;
in vec3 p3d_Normal;

// Output to fragment shader
out vec2 texcoord;
out vec3 normal;

void main() {
  ivec3 texelCoords = ivec3(
         gl_InstanceID % gridSize,
        (gl_InstanceID / gridSize)%gridSize,
         gl_InstanceID / (gridSize*gridSize));

  vec4 locationOffset = imageLoad(InstancingData, texelCoords);

  gl_Position = p3d_ModelViewProjectionMatrix*(locationOffset*(snoise(mouseTime.z*0.1+locationOffset.xyz*0.01*mouseTime.x)+1)*mouseTime.y + p3d_Vertex);

  normal = p3d_Normal;
  texcoord = p3d_MultiTexCoord0;
}
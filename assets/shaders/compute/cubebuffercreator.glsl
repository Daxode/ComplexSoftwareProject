#version 430
#define SIZE 8
#pragma include "../../external_libs/glsl-noise/simplex/three_d.glsl"

layout (local_size_x = 16, local_size_y = SIZE, local_size_z = SIZE) in;
uniform float spacing;
uniform float midPoint;

uniform writeonly image3D vertexBuffer;
void main() {
    vec4 point = (vec4(gl_GlobalInvocationID.xyz, 0)*spacing-vec4(midPoint,midPoint,midPoint,0));
    imageStore(vertexBuffer, ivec3(gl_GlobalInvocationID.xyz), point);
}
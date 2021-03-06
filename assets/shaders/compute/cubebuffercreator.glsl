#version 430
#define SIZE 8
#pragma include "../../external_libs/glsl-noise/simplex/three_d.glsl"

layout (local_size_x = 16, local_size_y = SIZE, local_size_z = SIZE) in;
uniform float spacing;

uniform writeonly image3D vertexBuffer;
void main() {
    vec3 point = gl_GlobalInvocationID.xyz*spacing;
    imageStore(vertexBuffer, ivec3(gl_GlobalInvocationID.xyz), vec4(point, 0.5));
}
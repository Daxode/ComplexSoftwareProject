#version 430
#define SIZE 8
#pragma include "../../external_libs/glsl-noise/simplex/three_d.glsl"

layout (local_size_x = 16, local_size_y = SIZE, local_size_z = SIZE) in;
uniform float radius;

layout(rgba32f, binding = 0) uniform image3D vertexBuffer;
void main() {
    vec4 point = imageLoad(vertexBuffer, ivec3(gl_GlobalInvocationID.xyz));
    point.w = (radius - length(point))/10 + snoise(point.xyz)*2;
    imageStore(vertexBuffer, ivec3(gl_GlobalInvocationID.xyz), point);
}
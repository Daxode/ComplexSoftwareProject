#version 430
#define SIZE 8
#pragma include "../../external_libs/glsl-noise/simplex/three_d.glsl"

layout (local_size_x = 16, local_size_y = SIZE, local_size_z = SIZE) in;
uniform float radius;
uniform float offset;
uniform vec3 midPoint;

layout(rgba32f, binding = 0) uniform image3D vertexBufferWAlpha;
void main() {
    vec4 point = imageLoad(vertexBufferWAlpha, ivec3(gl_GlobalInvocationID.xyz));
    point.w = (radius - length(point.xyz-midPoint))/10 + snoise(point.xyz+offset)*2;
    imageStore(vertexBufferWAlpha, ivec3(gl_GlobalInvocationID.xyz), point);
}
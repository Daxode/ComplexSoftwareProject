#version 430
#extension GL_ARB_compute_variable_group_size : enable
#define SIZE 512
layout (local_size_x = SIZE, local_size_y = 1) in;

uniform /*readonly*/ int gridSize;
uniform /*readonly*/ float radius;
uniform /*readonly*/ vec3[SIZE] fromVertexes;
 /*writeonly*/ vec3[SIZE] toVertexes;
uniform writeonly image1D kage;

vec3 spherize(vec3 cubeCord) {
    vec3 p = cubeCord * 2.0 / gridSize - vec3(1,1,1);
    vec3 p2 = vec3(p.x*p.x, p.y*p.y, p.z*p.z);
    return vec3(
        p.x * sqrt(1.0 - 0.5 * (p2.y + p2.z) + p2.y * p2.z / 3.0),
        p.y * sqrt(1.0 - 0.5 * (p2.z + p2.x) + p2.z * p2.x / 3.0),
        p.z * sqrt(1.0 - 0.5 * (p2.x + p2.y) + p2.x * p2.y / 3.0)
    )*radius;
}

void main() {
    toVertexes[gl_GlobalInvocationID.x] = spherize(fromVertexes[gl_GlobalInvocationID.x]);
    //imageStore(kage, ivec2(gl_GlobalInvocationID.x), vec3(1,1,0));
}
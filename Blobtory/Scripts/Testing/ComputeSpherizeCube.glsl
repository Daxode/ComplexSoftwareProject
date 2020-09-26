#version 430
#extension GL_ARB_compute_variable_group_size : enable
#define SIZE 512
layout (local_size_x = SIZE, local_size_y = 1) in;

uniform int gridSize;
uniform float radius;
layout(rgba32f, binding = 0) uniform readonly image1D fromVertexes;
layout(rgba32f, binding = 0) uniform writeonly image1D toVertexes;

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
    // Read the pixel from the first texture.
    vec4 pixel = imageLoad(fromVertexes, int(gl_GlobalInvocationID.x));
    // Swap the red and green channels.
    pixel = vec4(spherize(pixel.xyz), 1);

    // Now write the modified pixel to the second texture.
    imageStore(toVertexes, int(gl_GlobalInvocationID.x), pixel);
    //toVertexes[gl_GlobalInvocationID.x] = spherize(fromVertexes[gl_GlobalInvocationID.x]);
    //imageStore(kage, ivec2(gl_GlobalInvocationID.x), vec3(1,1,0));
}
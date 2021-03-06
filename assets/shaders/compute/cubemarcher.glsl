#version 430
#define SIZE 8
#pragma include "includes/MarchTables.glsl"

layout (local_size_x = 16, local_size_y = SIZE, local_size_z = SIZE) in;

layout(r32i) uniform iimageBuffer triagIndexBuffer;
layout(r32i) uniform readonly iimage2D triangulationBuffer;
layout(rgba32f) uniform readonly image3D vertexBufferWAlphaCube;
layout(rgba32f) uniform readonly image3D vertexBufferEdge;

uniform writeonly iimageBuffer triangleBuffer;
uniform writeonly imageBuffer normalBuffer;
uniform float isoLevel;
uniform bool isWater;
uniform ivec3 size;


void main() {
    // Stop one point before the end because voxel includes neighbouring points
    ivec3 id = ivec3(gl_GlobalInvocationID.xyz);
    if (id.x >= size.x-1 || id.y >= size.y-1 || id.z >= size.z-1) {
        return;
    }

    vec4 cubeCorners[8] = {
        imageLoad(vertexBufferWAlphaCube, id+ivec3(0,0,0)),
        imageLoad(vertexBufferWAlphaCube, id+ivec3(1,0,0)),
        imageLoad(vertexBufferWAlphaCube, id+ivec3(1,0,1)),
        imageLoad(vertexBufferWAlphaCube, id+ivec3(0,0,1)),
        imageLoad(vertexBufferWAlphaCube, id+ivec3(0,1,0)),
        imageLoad(vertexBufferWAlphaCube, id+ivec3(1,1,0)),
        imageLoad(vertexBufferWAlphaCube, id+ivec3(1,1,1)),
        imageLoad(vertexBufferWAlphaCube, id+ivec3(0,1,1))
    };

    int cubeIndex = 0;
    if (cubeCorners[0].w < isoLevel) cubeIndex |= 1;
    if (cubeCorners[1].w < isoLevel) cubeIndex |= 2;
    if (cubeCorners[5].w < isoLevel) cubeIndex |= 4;
    if (cubeCorners[4].w < isoLevel) cubeIndex |= 8;
    if (cubeCorners[3].w < isoLevel) cubeIndex |= 16;
    if (cubeCorners[2].w < isoLevel) cubeIndex |= 32;
    if (cubeCorners[6].w < isoLevel) cubeIndex |= 64;
    if (cubeCorners[7].w < isoLevel) cubeIndex |= 128;

    float wComb = 0;
    for (int i = 0; i < 8; i++) wComb += cubeCorners[i].w;

    int i = 0;
    int triangleEdgeIndex = 1;
    do {
        triangleEdgeIndex = imageLoad(triangulationBuffer, ivec2(i, cubeIndex)).x;
        if (triangleEdgeIndex == -1) return;

        ivec4 globalIndexForA = globalEdgeFromLocal[triangleEdgeIndex];
        ivec4 vertexID = ivec4(id+globalIndexForA.xyz+(ivec3(size.x, 0, 0)*globalIndexForA.w), 0);
        int triangleIDIndex = imageAtomicAdd(triagIndexBuffer, 0, 3);
        imageStore(triangleBuffer, triangleIDIndex, vertexID);
        vec3 v0 = imageLoad(vertexBufferEdge, vertexID.xyz).xyz;

        ivec4 globalIndexForB = globalEdgeFromLocal[imageLoad(triangulationBuffer, ivec2(i+1, cubeIndex)).x];
        vertexID = ivec4(id+globalIndexForB.xyz+(ivec3(size.x, 0, 0)*globalIndexForB.w), 0);
        imageStore(triangleBuffer, triangleIDIndex+1, vertexID);
        vec3 v1 = imageLoad(vertexBufferEdge, vertexID.xyz).xyz;

        ivec4 globalIndexForC = globalEdgeFromLocal[imageLoad(triangulationBuffer, ivec2(i+2, cubeIndex)).x];
        vertexID = ivec4(id+globalIndexForC.xyz+(ivec3(size.x, 0, 0)*globalIndexForC.w), 0);
        imageStore(triangleBuffer, triangleIDIndex+2, vertexID);
        vec3 v2 = imageLoad(vertexBufferEdge, vertexID.xyz).xyz;

        vec3 normal = normalize(cross(v2-v0, v1-v0));
        //vec3 normal = normalize(v2+v0+v1);
        int type = int(distance(vec3(512), v1)/51);
        if (isWater) type = 13; //int(sin(dot(normal,vec3(1)))*1+13);
        // if(type > 7) if(dot(normalize(vec3(512)-v1), normal)<0.5) type = 6;
        imageStore(normalBuffer, int(triangleIDIndex/3), vec4(normal, type));

        i+=3;
    } while (triangleEdgeIndex != -1);
}

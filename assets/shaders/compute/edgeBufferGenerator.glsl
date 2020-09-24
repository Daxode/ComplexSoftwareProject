#version 430
#define SIZE 8
#pragma include "../../external_libs/glsl-noise/simplex/three_d.glsl"

layout (local_size_x = 16, local_size_y = SIZE, local_size_z = SIZE) in;
uniform float isoLevel;
uniform ivec3 size;

//layout(binding = 0, offset = 12) uniform atomic_uint one;

vec3 interpolateVerts(vec4 v1, vec4 v2) {
    float t = 0.5;
    if (v1.w-v2.w < 0) {t=(isoLevel - v1.w) / (v2.w - v1.w);}
    else {t=(isoLevel - v2.w) / (v1.w - v2.w);}
    if (isinf(t)){t = 0.5;}
    t=0.5;
    return v1.xyz + t * (v2.xyz-v1.xyz);
}

layout(rgba32f) uniform readonly image3D vertexBufferWAlphaCube;
uniform writeonly image3D vertexBufferEdge;

void main() {
    ivec3 index = ivec3(gl_GlobalInvocationID.xyz);
    int type = int(gl_GlobalInvocationID.x/size.x);

    //uint currentIndex = atomicCounterIncrement(one);

    vec4 pointA = vec4(0);
    vec4 pointB = vec4(0);

    if (type == 0) {
        pointA = imageLoad(vertexBufferWAlphaCube, index);
        if (gl_GlobalInvocationID.x < size.x) {
            pointB = imageLoad(vertexBufferWAlphaCube, index+ivec3(1, 0, 0));
        }
    } else if (type == 1) {
        index.x = index.x-size.x;
        pointA = imageLoad(vertexBufferWAlphaCube, index);
        if (gl_GlobalInvocationID.y < size.y) {
            //pointB.xyz = index+ivec3(0,1,0);
            pointB = imageLoad(vertexBufferWAlphaCube, index+ivec3(0, 1, 0));
        }
    } else if (type == 2) {
        index.x = index.x-(size.x*2);
        pointA = imageLoad(vertexBufferWAlphaCube, index);
        if (gl_GlobalInvocationID.z < size.z) {
            pointB = imageLoad(vertexBufferWAlphaCube, index+ivec3(0, 0, 1));
        }
    }

    vec3 interpolatedVert = vec3(0);
    if (pointB != vec4(0)) {
        //interpolatedVert = pointB.xyz;
        //interpolatedVert = pointA.xyz + (0.5 * (pointB.xyz-pointA.xyz));
        interpolatedVert = interpolateVerts(pointA, pointB);
    }

    vec4 point = vec4(interpolatedVert, 0);
    imageStore(vertexBufferEdge, ivec3(gl_GlobalInvocationID.xyz), point);
}
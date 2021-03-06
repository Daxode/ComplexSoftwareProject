#version 430
#define SIZE 8
#pragma include "../../external_libs/glsl-noise/simplex/three_d.glsl"
#define PI 3.1415926535897932384626433832795

layout (local_size_x = 16, local_size_y = SIZE, local_size_z = SIZE) in;
uniform float radius;
uniform float offset;
uniform vec3 center;
uniform vec4 mouseTime;
const int craterCount = 000;

layout(rgba32f, binding = 0) uniform image3D vertexBufferWAlpha;

float rand(float x){
    return fract(sin(x)*10);
}

float fractalNoise(vec3 point) {
    float noiseSum = 0;
    float amplitude = 1;
    float frequency = 2;

    for (int i = 0; i < 5; i++){
        noiseSum += snoise(point*frequency)*amplitude;
        frequency *= 2;
        amplitude *= 0.5;
    }

    return noiseSum;
}

void main() {
    vec4 point = imageLoad(vertexBufferWAlpha, ivec3(gl_GlobalInvocationID.xyz));

    float mouseX = mouseTime.x;
    if (mouseTime.x == 0)  mouseX = 0.1;

    float lengthFromCenter = distance(center, point.xyz);
    float noiseOuter = (1-abs(fractalNoise(normalize(point.xyz-center)*1)+1))*mouseTime.w;
    float planetRadius = radius+noiseOuter;
    point.w = smoothstep(0, 1, (planetRadius - lengthFromCenter)/100);


    float cometOffset = 0.8;
    float cometDiff = 50.5;
    float sizeMatters = 0.1;
    for (int i = 0; i < craterCount; i++) {
        float theta = rand((offset+i))*2*PI;
        float phi = rand((offset+i+200))*2*PI;

        float cometSize = rand((offset+i))*50+100;

        vec3 cartCraterNormal = vec3(sin(theta)*cos(phi), sin(theta)*sin(phi), cos(theta));
        vec3 cartCraterPosCenter = (planetRadius*cometOffset-cometDiff+cometSize*sizeMatters)*cartCraterNormal;
        vec3 cartCraterPosOffset = (planetRadius*cometOffset+cometSize*sizeMatters)*cartCraterNormal;

        point.w += smoothstep(0,1, max(0, (cometSize-distance(point.xyz, cartCraterPosCenter))/100));
        point.w -= smoothstep(0,1, max(0, (cometSize-cometDiff-distance(point.xyz, cartCraterPosOffset))/100))*5;
    }

    //point.w = dot(sin(movedPoint.xyz*0.05)*0.3, vec3(1));

    imageStore(vertexBufferWAlpha, ivec3(gl_GlobalInvocationID.xyz), point);
}
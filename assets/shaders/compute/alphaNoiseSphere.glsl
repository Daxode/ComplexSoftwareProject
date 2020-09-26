#version 430
#define SIZE 8
#pragma include "../../external_libs/glsl-noise/simplex/three_d.glsl"

layout (local_size_x = 16, local_size_y = SIZE, local_size_z = SIZE) in;
uniform float radius;
uniform float offset;
uniform vec3 midPoint;
uniform vec3 mouseTime;

layout(rgba32f, binding = 0) uniform image3D vertexBufferWAlpha;
void main() {
    vec4 point = imageLoad(vertexBufferWAlpha, ivec3(gl_GlobalInvocationID.xyz));
    vec3 movedPoint = point.xyz-midPoint;

    float mouseX = mouseTime.x;
    if (mouseTime.x == 0)  mouseX = 0.1;

    float r = length(movedPoint);
//    float phi = atan(movedPoint.y/movedPoint.x);
//    float theta = acos(movedPoint.z/r)+mouseTime.y;
//    vec3 polarCoord = vec3(r, phi, theta);

//    point.w = (snoise(polarCoord.yz/(mouseX*10))*radius - r);
    float noiseOuter = (snoise((mouseTime.z/10)+normalize(movedPoint)*mouseX)+1)*10;
    float noiseInner = (snoise(normalize(movedPoint)*5+vec3(r/10))+1)*1;
    point.w = (radius - r)+(noiseOuter+noiseInner);
    //point.w = (radius - r)+snoise(movedPoint)*mouseTime.x*100;
    imageStore(vertexBufferWAlpha, ivec3(gl_GlobalInvocationID.xyz), point);
}
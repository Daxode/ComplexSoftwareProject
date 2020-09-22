#version 430

#pragma include "three_d.glsl"

layout (local_size_x = 512, local_size_y = 1) in;

// Declare the texture inputs
layout(rgba32f, binding=0) uniform readonly image2D fromTex;
uniform writeonly image2D toTex;
uniform vec3[] kage;
uniform vec2 mouse;

uniform writeonly imageBuffer someimg;

void main() {
    // Acquire the coordinates to the texel we are to process.

    ivec2 texelCoords = ivec2(gl_GlobalInvocationID.x / 512, gl_GlobalInvocationID.x % 512);
    //ivec2 texelCoords = ivec2(gl_GlobalInvocationID.xy);

    // Read the pixel from the first texture.
    vec4 pixel = imageLoad(fromTex, texelCoords);

    // Swap the red and green channels.
    // pixel.rg = vec2(gl_GlobalInvocationID.xy)*0.001;
    if (texelCoords.x < 256) {
        vec3 samplePoint = vec3(texelCoords, kage[1].x*1000);
        float noise = snoise(samplePoint*0.001*mouse.x)*100*mouse.y*100;
        float warpedNoise = snoise((samplePoint+vec3(noise, noise, noise))*0.01);
        warpedNoise = (warpedNoise+1)/2;
        pixel = vec4(vec3(warpedNoise, 0, 0), 1);
    } else {
        if (texelCoords.y < 256){
            pixel = vec4(kage[1], 1);
        }
    }
    //if (texelCoords == (mouse-1)*512) {
        // Now write the modified pixel to the second texture.
        imageStore(toTex, texelCoords, pixel);
    //}
    imageStore(someimg, texelCoords.x, vec4(texelCoords.xy, kage[1].x, 2));
}
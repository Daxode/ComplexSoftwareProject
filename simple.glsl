#version 430
layout (local_size_x = 2, local_size_y = 256) in;

// Declare the texture inputs
layout(rgba32f, binding=0) uniform readonly image2D fromTex;
uniform writeonly image2D toTex;
uniform vec3[] kage;

layout (binding = 1) writeonly buffer block2
{
    vec3 output_data[];
};

void main() {
  // Acquire the coordinates to the texel we are to process.

  //ivec2 texelCoords = ivec2(gl_GlobalInvocationID.x / 512, gl_GlobalInvocationID.x % 512);
  ivec2 texelCoords = ivec2(gl_GlobalInvocationID.xy);

  // Read the pixel from the first texture.
  vec4 pixel = imageLoad(fromTex, texelCoords);

  // Swap the red and green channels.
  // pixel.rg = vec2(gl_GlobalInvocationID.xy)*0.001;
  if (texelCoords.x < 256) {
      pixel = vec4(kage[0], 1);
  } else {
      if (texelCoords.y < 256){
          pixel = vec4(kage[1], 1);
      }
      output_data[texelCoords.x] = vec3(texelCoords.xy, kage[0].x);
  }

  // Now write the modified pixel to the second texture.
  imageStore(toTex, texelCoords, pixel);
}
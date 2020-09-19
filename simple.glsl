#version 430
layout (local_size_x = 512, local_size_y = 1) in;

// Declare the texture inputs
layout(rgba32f, binding=0) uniform readonly image2D fromTex;
uniform writeonly image2D toTex;

void main() {
  // Acquire the coordinates to the texel we are to process.
  ivec2 texelCoords = ivec2(gl_GlobalInvocationID.x / 512, gl_GlobalInvocationID.x % 512);

  // Read the pixel from the first texture.
  vec4 pixel = imageLoad(fromTex, texelCoords);

  // Swap the red and green channels.
  pixel.rg = vec2(gl_GlobalInvocationID.xy)*0.001;

  // Now write the modified pixel to the second texture.
  imageStore(toTex, texelCoords, pixel);
}
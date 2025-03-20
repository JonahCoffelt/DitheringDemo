#version 330 core

layout (location = 0) out vec4 fragColor;


in vec2 uv;

uniform sampler2D screenTexture;
uniform vec2 viewportDimensions;

vec3 sharpen() {
    vec2 offset = 1.0 / viewportDimensions;  

    // List of offsets used for sampling the texture
    vec2 offsets[9] = vec2[](
        vec2(-1.0, -1.0) * offset,
        vec2(-1.0,  0.0) * offset,
        vec2(-1.0,  1.0) * offset,
        vec2( 0.0, -1.0) * offset,
        vec2( 0.0,  0.0) * offset,
        vec2( 0.0,  1.0) * offset,
        vec2( 1.0, -1.0) * offset,
        vec2( 1.0,  0.0) * offset,
        vec2( 1.0,  1.0) * offset 
    );

    float kernel[9] = float[](
         0, -1,  0,
        -1,  5, -1,
         0, -1,  0
    );

    vec3 total = vec3(0.0);
    for (int i = 0; i < 9; i++)
    {
       total += texture(screenTexture, clamp(uv + offsets[i], 0.001, 0.999)).rgb * kernel[i];
    }

    return total;
}

void main() {
    vec3 color = sharpen();

    fragColor = vec4(color, 1.0);
}
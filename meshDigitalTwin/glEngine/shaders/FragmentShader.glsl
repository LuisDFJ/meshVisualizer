#version 330

in float istress;
out vec4 outColor;

vec3 hsv2rgb( vec3 c );

void main() {
    vec3 rgb = hsv2rgb( vec3( 0.6f * ( 1.0f - istress ), 1.0f, 1.0f ) );
    outColor = vec4( rgb, 1.0f);
}

vec3 hsv2rgb(vec3 c)
{
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}
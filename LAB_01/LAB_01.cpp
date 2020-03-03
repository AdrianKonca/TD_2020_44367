#include <iostream>

const float A = 7;
const float B = 6;
const float C = 3;
const float D = 4;
const float E = 4;

float x(float t)
{
	return A * t * t + B * t + C;
}

void taskOne(float startT, float endT, float deltaT)
{

}

void taskTwo(float startT, float endT, float deltaT)
{

}

int main()
{
	taskOne(-10, 10, 1 / 100);
	taskTwo(-1, 1, 1 / 22050);
}
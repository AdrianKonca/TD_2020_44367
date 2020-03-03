#include <iostream>
#include <vector>

const float A = 7;
const float B = 6;
const float C = 3;
const float D = 4;
const float E = 4;

float x(float t)
{
	return A * t * t + B * t + C;
}

void solveSquareEquation(float a, float b, float c)
{
	auto discriminant = b * b - 4 * a * c;
	if (discriminant < 0)
		std::cout << "There are no roots.";
	else if (discriminant == 0)
		std::cout << "There is only one root. x = " << (-b / 2 * a);
	else
		std::cout << "There are two roots. x1 = " << ((-b - sqrt(discriminant)) / 2 * a) << " x2 = " << ((-b + sqrt(discriminant)) / 2 * a);
}

std::vector<float> solveFunction(std::vector<float> arguments, float (*f)(float))
{
	std::vector<float> results;
	for (auto argument : arguments)
		results.push_back(f(argument));
	return results;
}

std::vector<float> fillVector(float startT, float endT, float deltaT)
{
	std::vector<float> range;
	auto t = startT;
	while (t <= endT)
	{
		range.push_back(t);
		t += deltaT;
	}
	return range;
}

void saveResult(std::vector<float> arguments, std::vector<float> results, std::string filename)
{

}

void taskOne(float startT, float endT, float deltaT)
{
	solveSquareEquation(A, B, C);
}

void taskTwo(float startT, float endT, float deltaT)
{

}

int main()
{
	taskOne(-10, 10, 1 / 100);
	taskTwo(-1, 1, 1 / 22050);
}
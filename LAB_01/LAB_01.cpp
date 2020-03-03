#include <iostream>
#include <fstream>
#include <vector>

const double A = 7;
const double B = 6;
const double C = 3;
const double D = 4;
const double E = 4;

double x(double t)
{
	return A * t * t + B * t + C;
}

void solveSquareEquation(double a, double b, double c)
{
	auto discriminant = b * b - 4 * a * c;
	if (discriminant < 0)
		std::cout << "There are no roots.";
	else if (discriminant == 0)
		std::cout << "There is only one root. x = " << (-b / 2 * a);
	else
		std::cout << "There are two roots. x1 = " << ((-b - sqrt(discriminant)) / 2 * a) << " x2 = " << ((-b + sqrt(discriminant)) / 2 * a);
}

std::vector<double> solveFunction(std::vector<double> arguments, double (*function)(double))
{
	std::vector<double> results;
	for (auto argument : arguments)
		results.push_back(function(argument));
	return results;
}

std::vector<double> fillVector(double startT, double endT, double deltaT)
{
	std::vector<double> range;
	auto t = startT;
	while (t <= endT)
	{
		range.push_back(t);
		t += deltaT;
	}
	return range;
}

void saveResult(std::vector<double> arguments, std::vector<double> results, std::string filename)
{

}

void taskOne(double startT, double endT, double deltaT)
{
	solveSquareEquation(A, B, C);
}

void taskTwo(double startT, double endT, double deltaT)
{

}

int main()
{
	taskOne(-10, 10, 1.0 / 100.0);
	taskTwo(-1, 1, 1,0 / 22050.0);
}
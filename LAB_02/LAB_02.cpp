#include <iostream>
#include <vector>

#define PI 3.14159265358979323846

const double A = 7;
const double B = 6;
const double C = 3;
const double D = 4;
const double E = 4;

double s(double t)
{
    const double A = 1.0;
    const double F = B;
    const double PHI = C * PI;
    return A * sin(2 * PI * F * t + PHI);
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
	std::ofstream file("Outputs/" + filename);
	file << "t, y\n";
	for (auto i = 0; i < arguments.size(); i++)
	{
		file << arguments.at(i) << "," << results.at(i) << "\n";
	}
	file.flush();
	file.close();
}

int main()
{
    std::cout << "Hello World!\n";
}
#include <iostream>
#include <fstream>
#include <vector>

#define PI 3.14159265358979323846

const double A = 7;
const double B = 6;
const double C = 3;
const double D = 4;
const double E = 4;

const double AMPLITUDE = 1.0;

double s(double t)
{
    const double F = B;
    const double PHI = C * PI;
    return AMPLITUDE * sin(2 * PI * F * t + PHI);
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

int Quantization(double value, double maxValue)
{
	return round((value + AMPLITUDE) * (maxValue - 1) / 2);
}

std::vector<int> QuantizyRange(std::vector<double> values, int maxValue)
{
	std::vector<int> quantizedRange;
	for (auto i = 0; i < values.size(); i++)
	{
		quantizedRange.push_back(Quantization(values.at(i), maxValue));
	}
	return quantizedRange;
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

void saveResult(std::vector<double> arguments, std::vector<int> results, std::string filename)
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
	double startT = 0;
	double stopT = A;
	double deltaT = 0.01;
	double fs = 1 / deltaT;
	
	auto arguments = fillVector(startT, stopT, deltaT);
	auto results = solveFunction(arguments, s);
	saveResult(arguments, results, "s.csv");
}
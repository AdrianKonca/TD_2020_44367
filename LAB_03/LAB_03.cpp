#include <iostream>
#include <fstream>
#include <vector>
#include <complex>

#define PI 3.14159265358979323846

const double A = 7;
const double B = 6;
const double C = 3;
const double D = 4;
const double E = 4;

const double AMPLITUDE = 1.0;
const double FREQUENCY = B;
const double PHASE_ANGLE = C * PI;

double s(double t)
{
	return AMPLITUDE * sin(2 * PI * FREQUENCY * t + PHASE_ANGLE);
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

void fullPrecision(double startT, double endT, double deltaT, int q)
{
	auto arguments = fillVector(startT, endT, deltaT);
	auto results = solveFunction(arguments, s);
	saveResult(arguments, results, "s.csv");
	auto quantized = QuantizyRange(results, 2 << (q - 1));
	saveResult(arguments, quantized, "sQuantized.csv");
}

void halfPrecision(double startT, double endT, double deltaT, int q)
{
	auto arguments = fillVector(startT, endT, deltaT * 2);
	auto results = solveFunction(arguments, s);
	auto quantized = QuantizyRange(results, 2 << (q - 1));
	saveResult(arguments, quantized, "sQuantizedHalf.csv");
}

std::vector<std::complex<double>> discreteFourierTransformation(std::vector <double> samples)
{

}

int main()
{
	const int q = 16;
	double startT = 0.0;
	double stopT = A;
	const double fs = 1000.0;
	double deltaT = 1.0 / fs;

	fullPrecision(startT, stopT, deltaT, q);
	halfPrecision(startT, stopT, deltaT, q / 2);
}
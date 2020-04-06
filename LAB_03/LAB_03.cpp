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

struct FileRow
{
	double t;
	double y;
};

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

template <typename T, typename X>
void saveResult(std::vector<T> arguments, std::vector<X> results, std::string filename)
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

std::vector<std::complex<double>> discreteFourierTransformation(std::vector <double> samples)
{
	std::complex<double> J(0, 1);
	int samplesCount = samples.size();
	std::vector<std::complex<double>> transformedSamples(samplesCount);
	for (auto i = 0; i < samplesCount; ++i)
	{
		transformedSamples[i] = std::complex<double>(0, 0);
		for (auto j = 0; j < samplesCount; ++j)
			transformedSamples[i] += samples[j] * exp(J * -PI * 2.0 * (double)i * (double)j / (double)samplesCount);
	}
	return transformedSamples;
}

std::vector<double> frequencyScaleCalculator(double samplingFrequency, int samplesCount)
{
	std::vector<double> frequencies(samplesCount);
	for (auto i = 0; i < samplesCount; ++i)
		frequencies[i] = (double)i * samplingFrequency / (double)samplesCount;
	return frequencies;
}

std::vector<double> getFirstHalfOfVector(std::vector<double> vectorToSplit)
{
	std::vector<double> firstHalf(vectorToSplit.begin(), vectorToSplit.begin() + vectorToSplit.size() / 2);
	return firstHalf;
}

std::vector <double> invertedDiscreteFourierTransformation(std::vector<std::complex<double>> transformedSamples)
{
	int SAMPLES_COUNT = transformedSamples.size();
	std::complex<double> J(0, 1);
	std::vector<double> samples(SAMPLES_COUNT);
	for (auto i = 0; i < SAMPLES_COUNT; ++i)
	{
		samples[i] = 0;
		for (auto j = 0; j < SAMPLES_COUNT; ++j)
			samples[i] += (transformedSamples[j] * exp(J * PI * 2.0 * (double)i * (double)j / (double)SAMPLES_COUNT)).real();
		samples[i] /= (double)SAMPLES_COUNT;
	}
	return samples;
}

std::vector<double> amplitudeSpectrumTransformation(std::vector<std::complex<double>> transformedSamples)
{
	std::vector<double> amplitudes(transformedSamples.size());
	for (auto i = 0; i < transformedSamples.size(); ++i)
		amplitudes[i] = abs(transformedSamples[i]) / transformedSamples.size() * 2;
	return amplitudes;
}

std::vector<FileRow> readInputFile(std::string filename)
{

	std::ifstream dataFile("Inputs/" + filename);
	std::vector<FileRow> fileRows;

	double t, y;
	char delimiter;
	
	//ignore first line
	dataFile.ignore(1000, '\n');

	while (dataFile >> t >> delimiter >> y)
		fileRows.push_back({t, y});
	
	return fileRows;
}

std::vector<FileRow> getEveryNthSample(std::vector<FileRow> values, int samplesCount)
{
	auto step = (double)values.size() / (double)samplesCount;
	double currentStep = 0;
	std::vector<FileRow> nthValues;
	for (auto i = 0; i < samplesCount; i++)
	{
 		nthValues.push_back(values[round(currentStep)]);
		currentStep += step;
	}
	return nthValues;
}

std::vector<double> getTValuesColumn(std::vector<FileRow> values)
{
	std::vector<double> tValues(values.size());
	for (auto i = 0; i < values.size(); i++)
		tValues[i] = values[i].t;
	return tValues;
}

std::vector<double> getYValuesColumn(std::vector<FileRow> values)
{
	std::vector<double> yValues(values.size());
	for (auto i = 0; i < values.size(); i++)
		yValues[i] = values[i].y;
	return yValues;
}

void secondAndFourthTask()
{
	const double STARTING_T = 0.0;
	const double SAMPLING_FREQENCY = 1000;
	const double DELTA_T = 1.0 / SAMPLING_FREQENCY;
	const double SAMPLE_COUNT = A * 100 + B * 10 + C;
	const double FINISHING_T = SAMPLE_COUNT * DELTA_T;

	auto tValues = fillVector(STARTING_T, FINISHING_T, DELTA_T);
	auto sValues = solveFunction(tValues, s);
	auto sTransformed = discreteFourierTransformation(sValues);
	auto sAmplitudes = getFirstHalfOfVector(amplitudeSpectrumTransformation(sTransformed));
	auto frequencyScale = getFirstHalfOfVector(frequencyScaleCalculator(SAMPLING_FREQENCY, sTransformed.size()));
	auto sValuesReversed = invertedDiscreteFourierTransformation(sTransformed);
	saveResult<double, double>(tValues, sValues, "s.csv");
	saveResult<double, double>(frequencyScale, sAmplitudes, "sAmplitudes.csv");
	saveResult<double, double>(tValues, invertedDiscreteFourierTransformation(sTransformed), "sReversed.csv");
	saveResult<double, double>(tValues, sValuesReversed, "sReversed.csv");
}

void thirdSubTask(std::string filename)
{
	const double SAMPLE_COUNT = A * 100 + B * 10 + C;
	const double SAMPLING_FREQENCY = 22050;
	auto values = getEveryNthSample(readInputFile(filename + ".csv"), SAMPLE_COUNT);
	auto tValues = getTValuesColumn(values);
	auto yValues = getYValuesColumn(values);
	
	auto yTransformed = discreteFourierTransformation(yValues);
	auto yAmplitudes = getFirstHalfOfVector(amplitudeSpectrumTransformation(yTransformed));
	auto frequencyScale = getFirstHalfOfVector(frequencyScaleCalculator(SAMPLING_FREQENCY, yTransformed.size()));
	saveResult<double, double>(tValues, yValues, filename + ".csv");
	saveResult<double, double>(frequencyScale, yAmplitudes, filename + "Amplitudes.csv");
}
void thirdTask()
{
	thirdSubTask("p2");
	thirdSubTask("p4");
	thirdSubTask("pAB");
	thirdSubTask("x");
	thirdSubTask("y");
	thirdSubTask("v");
	thirdSubTask("z");
	thirdSubTask("u");
}

int main()
{
	secondAndFourthTask();
	thirdTask();
}
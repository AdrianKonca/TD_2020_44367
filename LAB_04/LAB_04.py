import numpy as np
import matplotlib.pyplot as plt

A = 7
B = 6
C = 3
D = 4
E = 4

AMPLITUDE = 1.0
FREQUENCY = 1

#Ka Modulation depth for AM
#Kp Modulation depth for PM
def informationSignal(t):
    return AMPLITUDE * np.sin(2 * np.pi * FREQUENCY * t)

def amplitudeModulation(samples, modulationDepth, modulationFrequency, t):
    return (modulationDepth + (samples + AMPLITUDE)) * np.cos(2 * np.pi * modulationFrequency * t)

def phaseModulation(samples, modulationDepth, modulationFrequency, t):
    return np.cos((2 * np.pi * modulationFrequency * t) + (modulationDepth * samples))

def filterNoise(filterParameter, amplitudes, frequencies):
    frequenciesFiltered = []
    amplitudesFiltered = []
    minimumAmplitude = max(amplitudes) / filterParameter
    for i, amplitude in enumerate(amplitudes):
        if (amplitude > minimumAmplitude):
            amplitudesFiltered.append(amplitude)
            frequenciesFiltered.append(frequencies[i])
    return frequenciesFiltered, amplitudesFiltered

def frequencyScaleCalculator(samplingFrequency, samplesCount):
	frequencies = []
	for i in range(samplesCount):
		frequencies.append(i * samplingFrequency / samplesCount)
	return np.array(frequencies)

def convertToDecibelScale(amplitudes):
    return np.log10(amplitudes) * 10

def convertFftToAmplitudeSpectrum(fftValues):
    return abs(np.array(fftValues))/len(fftValues)

def taskOne(amplitudeModulationDepth, phaseModulationDepth):
    SAMPLING_FREQUENCY = 10000

    t = np.linspace(0, 1, SAMPLING_FREQUENCY)

    samples = informationSignal(t)
    samplesAfterAmplitudeModulation = amplitudeModulation(samples, amplitudeModulationDepth, 100, t)
    samplesAfterPhaseModulation = phaseModulation(samples, phaseModulationDepth, 25, t)

    plt.figure(figsize = (16, 9))
    #plt.figure()
    plt.subplot(5, 1, 1)
    plt.scatter(t, samples, 1, color='tab:blue')
    plt.title("Pure tone")
    plt.xlabel("Time")
    plt.ylabel("Signal strength")
    plt.subplot(5, 1, 2)
    plt.scatter(t, samplesAfterAmplitudeModulation, 1, color='tab:blue')
    plt.title("Amplitude modulation")
    plt.xlabel("Time")
    plt.ylabel("Signal strength")
    plt.subplot(5, 1, 3)
    plt.scatter(t, samplesAfterPhaseModulation, 1, color='tab:blue')
    plt.title("Phase modulation")
    plt.xlabel("Time")
    plt.ylabel("Signal strength")

    fftAmplitude = np.fft.rfft(samplesAfterAmplitudeModulation)
    fftPhase = np.fft.rfft(samplesAfterPhaseModulation)

    frequency = frequencyScaleCalculator(SAMPLING_FREQUENCY, len(fftAmplitude))

    amplitudeSpectrum = convertFftToAmplitudeSpectrum(fftAmplitude)
    amplitudeFrequencies, amplitudeFilteredAmplitudeSpectrum = filterNoise(500, amplitudeSpectrum, frequency)

    phaseSpectrum = convertFftToAmplitudeSpectrum(fftPhase)
    phaseFrequencies, phaseFilteredAmplitudeSpectrum = filterNoise(500, phaseSpectrum, frequency)

    plt.subplot(5, 1, 4)
    plt.stem(amplitudeFrequencies, convertToDecibelScale(amplitudeFilteredAmplitudeSpectrum), markerfmt = 'C1o', use_line_collection=True)
    plt.title("Amplitude spectrum of AM")
    plt.ylabel('Decibels')
    plt.xlabel('Frequency')
    plt.subplot(5, 1, 5)
    plt.stem(phaseFrequencies, convertToDecibelScale(phaseFilteredAmplitudeSpectrum), markerfmt = 'C1o', use_line_collection=True)
    plt.title("Amplitude spectrum of PM")
    plt.ylabel('Decibels')
    plt.xlabel('Frequency')
    plt.tight_layout()





taskOne(0.5, 1)
taskOne(10, 3.14)
taskOne(100, 100)
plt.show()
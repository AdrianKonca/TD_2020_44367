import numpy as np
import matplotlib.pyplot as plt

A = 7
B = 6
C = 3
D = 4
E = 4

AMPLITUDE = 1.0
FREQUENCY = 4

#Ka Modulation depth for AM
#Kp Modulation depth for PM
def informationSignal(t):
    return AMPLITUDE * np.sin(2 * np.pi * FREQUENCY * t)

def carryingSignal(t, modulationFrequency):
    return np.cos(2 * np.pi * modulationFrequency * t)

def amplitudeModulation(samples, modulationDepth, modulationFrequency, t):
    carryingSignalSamples = carryingSignal(t, modulationFrequency)
    return carryingSignalSamples, (modulationDepth + (samples + AMPLITUDE)) * carryingSignalSamples

def phaseModulation(samples, modulationDepth, modulationFrequency, t):
    return carryingSignal(t, modulationFrequency), np.cos((2 * np.pi * modulationFrequency * t) + np.radians(modulationDepth * samples))

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
		frequencies.append(i * samplingFrequency / samplesCount / 2)
	return np.array(frequencies)

def convertToDecibelScale(amplitudes):
    return np.log10(amplitudes) * 10

def convertFftToAmplitudeSpectrum(fftValues):
    return abs(np.array(fftValues))/len(fftValues)

def drawModulation(t, modulationSamples, carryingSamples, modulationLabel, subplot):
    plt.subplot(5, 1, subplot)
    plt.scatter(t, carryingSamples, 1, color='tab:red', label = 'Carrier signal')
    plt.scatter(t, modulationSamples, 1, color='tab:blue', alpha=0.1, label = modulationLabel)
    plt.title("Amplitude modulation")
    plt.xlabel("Time")
    plt.ylabel("Signal strength")
    plt.legend()

def drawAmplitudeSpectrum(frequencies, amplitudeSamples, title, subplot):
    plt.subplot(5, 1, subplot)
    plt.stem(frequencies, convertToDecibelScale(amplitudeSamples), markerfmt = 'C1o', use_line_collection=True)
    plt.title(title)
    plt.ylabel('Decibels')
    plt.xlabel('Frequency')


def taskOne(amplitudeModulationDepth, phaseModulationDepth, filename):
    SAMPLING_FREQUENCY = 25000
    TIME = 1
    SAMPLES_COUNT = TIME * SAMPLING_FREQUENCY
    t = np.linspace(0, TIME, SAMPLES_COUNT)

    samples = informationSignal(t)
    amplitudeCarryingSamples, amplitudeModulationSamples = amplitudeModulation(samples, amplitudeModulationDepth, 100, t)
    phaseCarryingSamples, phaseModulationSamples = phaseModulation(samples, phaseModulationDepth, 40, t)
    
    plt.figure(figsize = (16, 9))
    plt.subplot(5, 1, 1)
    plt.scatter(t, samples, 1, color='tab:blue')
    plt.title("Pure tone")
    plt.xlabel("Time")
    plt.ylabel("Signal strength")
    drawModulation(t, amplitudeModulationSamples, amplitudeCarryingSamples, 'AM signal', 2)
    drawModulation(t, phaseModulationSamples, phaseCarryingSamples, 'PM signal', 4)

    fftAmplitude = np.fft.rfft(amplitudeModulationSamples)
    fftPhase = np.fft.rfft(phaseModulationSamples)

    frequency = frequencyScaleCalculator(SAMPLING_FREQUENCY, len(fftAmplitude))

    amplitudeSpectrum = convertFftToAmplitudeSpectrum(fftAmplitude)
    amplitudeFrequencies, amplitudeFilteredAmplitudeSpectrum = filterNoise(500, amplitudeSpectrum, frequency)

    phaseSpectrum = convertFftToAmplitudeSpectrum(fftPhase)
    phaseFrequencies, phaseFilteredAmplitudeSpectrum = filterNoise(500, phaseSpectrum, frequency)

    drawAmplitudeSpectrum(amplitudeFrequencies, amplitudeFilteredAmplitudeSpectrum, 'Amplitude spectrum of AM', 3)
    drawAmplitudeSpectrum(phaseFrequencies, phaseFilteredAmplitudeSpectrum, 'Amplitude spectrum of PM', 5)
    plt.tight_layout()
    plt.savefig('Charts/' + filename, dpi = 150)


taskOne(0.5, 1, "modulationA.png")
taskOne(10, 3.14, "modulationB.png")
taskOne(100, 90, "modulationC.png")
plt.show()

#Niebieski sygnał AM i PM rysowany jest z lekką alfą - ponieważ Carry Signal PM był bardzo podobny do PM.
#Ponadto, alfa ta pozwala zauważyć zagęszczenia w wartościach PM - zwłaszcza na wykresie C

#Zadanie 3
#A
#   fmin AM = 96Hz, fmax AM = 104Hz, W = 8Hz
#   fmin PM = 40Hz, fmax PM = 40Hz, W = 0Hz
#B
#   fmin AM = 96Hz, fmax AM = 104Hz, W = 8Hz
#   fmin PM = 40Hz, fmax PM = 40Hz, W = 0Hz
#C
#   fmin AM = 96Hz, fmax AM = 104Hz, W = 8Hz
#   fmin PM = 36Hz, fmax PM = 44Hz, W = 8Hz

#   Wydaje mi się, że im mniejsze W (szerokość pasma, bandwidth) tym lepiej dla sygnału radiowego, ponieważ zmniejsza on
#   ilość potrzebnych do obserwacji pasm oraz pozwala na puszczanie wielu sygnałów naraz (ale tak naprawde nie wiem czy 
#   jest to prawda, tak tylko mi się wydaje)
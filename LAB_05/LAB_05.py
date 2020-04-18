import matplotlib.pyplot as plt
import numpy as np

def stringToBinaryStream(text, littleEndian = False):
    binaryStream = []
    for character in (text):
        binaryCharacter = format(ord(character), '08b')
        for bit in (binaryCharacter):
            binaryStream.append(bit == '1')
    if littleEndian:
        return binaryStream[::-1]
    return binaryStream

AMPLITUDE_LOW = 0.1
AMPLITUDE_HIGH = 1
PHASE_LOW = 0
PHASE_HIGH = np.pi
SECONDS_PER_BIT = 0.1
FREQUENCY = 0
SAMPLES_PER_BIT = 400
FREQUENCY_LOW = 0
FREQUENCY_HIGH = 0

def recalculateFrequencyConstants(frequencyMultiplier):
    global FREQUENCY
    global FREQUENCY_LOW
    global FREQUENCY_HIGH
    FREQUENCY = frequencyMultiplier / SECONDS_PER_BIT
    FREQUENCY_LOW = (frequencyMultiplier + 1) / SECONDS_PER_BIT
    FREQUENCY_HIGH = (frequencyMultiplier + 2) / SECONDS_PER_BIT

def amplitudeShiftKeying(samples, time):
    AMPLITUDES = {False: AMPLITUDE_LOW, True: AMPLITUDE_HIGH}
    askSamples = []
    for s, t in zip(samples, time):
        askSamples.append(AMPLITUDES[s] * np.sin(2 * np.pi * FREQUENCY * t))
    return askSamples
        
def frequencyShiftKeying(samples, time):
    FREQUENCIES = {False: FREQUENCY_LOW, True: FREQUENCY_HIGH}
    fskSamples = []
    for s, t in zip(samples, time):
        fskSamples.append(np.sin(2 * np.pi * FREQUENCIES[s] * t))
    return fskSamples

def phaseShiftKeying(samples, time):
    PHASES = {False: PHASE_LOW, True: PHASE_HIGH}
    pskSamples = []
    for s, t in zip(samples, time):
        pskSamples.append(np.sin(2 * np.pi * FREQUENCY * t + PHASES[s]))
    return pskSamples

def informationSignal(secondsPerBit, bits, samplesPerBit):
    time = np.linspace(0, secondsPerBit * len(bits), samplesPerBit * len(bits))

    signalSamples = np.empty(samplesPerBit * len(bits), dtype = np.bool_)
    for i, bit in enumerate(bits):
        signalSamples[i * samplesPerBit:(i + 1) * samplesPerBit] = np.tile(bit, samplesPerBit)
    return time, signalSamples


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

def drawAmplitudeSpectrum(frequencies, amplitudeSamples, title, subplot):
    plt.subplot(3, 2, subplot)
    plt.stem(frequencies, convertToDecibelScale(amplitudeSamples), markerfmt = 'C1o', use_line_collection=True)
    plt.title(title)
    plt.ylabel('Decibels')
    plt.xlabel('Frequency')

def drawShiftKeyingPlot(time, samples, keyingSamples, keyingType):
    plt.plot(time, samples)
    plt.scatter(time, keyingSamples, 1)
    plt.title(keyingType + " shift keying")
    plt.ylabel("Amplitude")
    plt.xlabel("Time")

def taskOne():
    print(stringToBinaryStream("test", True))
    #Expected:
    #[False, False, True, False, True, True, True, False, True, True, False, False, True, True, True, False, True, False, True, False, False, True, True, False, False, False, True, False, True, True, True, False]
    print(stringToBinaryStream("test", False))
    #Expected
    #[False, True, True, True, False, True, False, False, False, True, True, False, False, True, False, True, False, True, True, True, False, False, True, True, False, True, True, True, False, True, False, False]

def taskTwo():
    FREQUENCY_MULTIPLIER = 1
    recalculateFrequencyConstants(FREQUENCY_MULTIPLIER)

    plt.figure(figsize = (16, 9))

    bits = stringToBinaryStream("Tak")
    time, s = informationSignal(SECONDS_PER_BIT, bits, SAMPLES_PER_BIT)
    fa = amplitudeShiftKeying(s, time)
    ff = frequencyShiftKeying(s, time)
    fs = phaseShiftKeying(s, time)
    plt.subplot(3, 1, 1)
    drawShiftKeyingPlot(time, s, fa, "Amplitude")
    plt.subplot(3, 1, 2)
    drawShiftKeyingPlot(time, s, ff, "Frequency")
    plt.subplot(3, 1, 3)
    drawShiftKeyingPlot(time, s, fs, "Phase")

    plt.tight_layout()
    plt.savefig('Charts/taskTwo.png', dpi = 150)

def taskThree():
    FREQUENCY_MULTIPLIER = 2
    BITS_COUNT = 10
    SAMPLING_FREQUENCY = SAMPLES_PER_BIT / SECONDS_PER_BIT
    recalculateFrequencyConstants(FREQUENCY_MULTIPLIER)

    plt.figure(figsize = (16, 9))

    bits = stringToBinaryStream("Tak")
    time, signalSamples = informationSignal(SECONDS_PER_BIT, bits, SAMPLES_PER_BIT)
    fa = amplitudeShiftKeying(signalSamples, time)
    ff = frequencyShiftKeying(signalSamples, time)
    fs = phaseShiftKeying(signalSamples, time)
    plt.subplot(3, 2, 1)
    drawShiftKeyingPlot(time[0:SAMPLES_PER_BIT*BITS_COUNT], signalSamples[0:SAMPLES_PER_BIT*BITS_COUNT], fa[0:SAMPLES_PER_BIT*BITS_COUNT], "Amplitude")
    plt.subplot(3, 2, 3)
    drawShiftKeyingPlot(time[0:SAMPLES_PER_BIT*BITS_COUNT], signalSamples[0:SAMPLES_PER_BIT*BITS_COUNT], ff[0:SAMPLES_PER_BIT*BITS_COUNT], "Frequency")
    plt.subplot(3, 2, 5)
    drawShiftKeyingPlot(time[0:SAMPLES_PER_BIT*BITS_COUNT], signalSamples[0:SAMPLES_PER_BIT*BITS_COUNT], fs[0:SAMPLES_PER_BIT*BITS_COUNT], "Phase")

    fftAmplitude = np.fft.rfft(fa)
    fftFrequency = np.fft.rfft(ff)
    fftPhase = np.fft.rfft(fs)

    frequency = frequencyScaleCalculator(SAMPLING_FREQUENCY, len(fftAmplitude))

    amplitudeSpectrum = convertFftToAmplitudeSpectrum(fftAmplitude)
    amplitudeFrequencies, amplitudeFilteredAmplitudeSpectrum = filterNoise(10, amplitudeSpectrum, frequency)

    frequencySpectrum = convertFftToAmplitudeSpectrum(fftFrequency)
    frequencyFrequencies, frequencyFilteredAmplitudeSpectrum = filterNoise(10, frequencySpectrum, frequency)

    phaseSpectrum = convertFftToAmplitudeSpectrum(fftPhase)
    phaseFrequencies, phaseFilteredAmplitudeSpectrum = filterNoise(10, phaseSpectrum, frequency)

    drawAmplitudeSpectrum(amplitudeFrequencies, amplitudeFilteredAmplitudeSpectrum, 'Amplitude spectrum of ASK', 2)
    drawAmplitudeSpectrum(frequencyFrequencies, frequencyFilteredAmplitudeSpectrum, 'Amplitude spectrum of FSK', 4)
    drawAmplitudeSpectrum(phaseFrequencies, phaseFilteredAmplitudeSpectrum, 'Amplitude spectrum of PSK', 6)

    plt.tight_layout()
    plt.savefig('Charts/taskThree.png', dpi = 150)

taskOne()
taskTwo()
taskThree()

#Szerokość pasma
    #ASK dla - 5Db
    #fmin = 20Hz
    #fmax = 20Hz
    #szerokość = 0Hz
    #FSK dla - 5Db
    #fmin = 30Hz
    #fmax = 40Hz
    #szerokość = 10Hz
    #PSK dla - 5Db
    #fmin = 15.8Hz
    #fmax = 15.8Hz
    #szerokość = 0Hz
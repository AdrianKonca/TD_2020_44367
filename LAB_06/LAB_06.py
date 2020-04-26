import matplotlib.pyplot as plt
import math as math

def stringToBinaryStream(text, littleEndian = False):
    binaryStream = []
    for character in (text):
        binaryCharacter = format(ord(character), '08b')
        for bit in (binaryCharacter):
            binaryStream.append(bit == '1')
    if littleEndian:
        return binaryStream[::-1]
    return binaryStream

#recreates tile function from numpy
def tile(value, count):
    return [value for _ in range(count)]

#recreates numpy linspace
def linspace(low, high, stepCount):
    step = (high - low) / (stepCount - 1)
    values = [low + step * i for i in range(stepCount)]
    return values

AMPLITUDE_LOW = 0
AMPLITUDE_HIGH = 1
PHASE_LOW = 0
PHASE_HIGH = math.pi
SECONDS_PER_BIT = 0.1
FREQUENCY = 0
SAMPLES_PER_BIT = 400
FREQUENCY_LOW = 0
FREQUENCY_HIGH = 0
COMPARATOR_THRESHOLD = 5

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
        askSamples.append(AMPLITUDES[s] * math.sin(2 * math.pi * FREQUENCY * t))
    return askSamples
        
def frequencyShiftKeying(samples, time):
    FREQUENCIES = {False: FREQUENCY_LOW, True: FREQUENCY_HIGH}
    fskSamples = []
    for s, t in zip(samples, time):
        fskSamples.append(math.sin(2 * math.pi * FREQUENCIES[s] * t))
    return fskSamples

def phaseShiftKeying(samples, time):
    PHASES = {False: PHASE_LOW, True: PHASE_HIGH}
    pskSamples = []
    for s, t in zip(samples, time):
        pskSamples.append(math.sin(2 * math.pi * FREQUENCY * t + PHASES[s]))
    return pskSamples
        
def informationSignal(secondsPerBit, bits, samplesPerBit):
    time = linspace(0, secondsPerBit * len(bits), samplesPerBit * len(bits))

    signalSamples = samplesPerBit * len(bits) * [None]
    for i, bit in enumerate(bits):
        signalSamples[i * samplesPerBit:(i + 1) * samplesPerBit] = tile(bit, samplesPerBit)
    return time, signalSamples

def drawShiftKeyingPlot(time, samples, keyingSamples, keyingType):
    plt.plot(time, samples)
    plt.scatter(time, keyingSamples, 1)
    plt.title(keyingType + " shift keying of m(t)")
    plt.ylabel("Amplitude")
    plt.xlabel("Time")

def demodulationASKandPSK(shiftKeyingSamples, productSamples):
    integralPerBitSum = []
    index = 0
    for _ in range(round(len(shiftKeyingSamples)/SAMPLES_PER_BIT)):
        integralPerBitSum.append(productSamples[index])
        index += 1
        for _ in range(1, SAMPLES_PER_BIT):
            integralPerBitSum.append(integralPerBitSum[index - 1] + productSamples[index])
            index += 1
    demodulatedInformationSamples = [integral >= COMPARATOR_THRESHOLD for integral in integralPerBitSum]
    return integralPerBitSum, demodulatedInformationSamples

def demodulationFSK(shiftKeyingSamples, productSamplesTrueOnly, productSamplesFalseOnly):
    integralPerBitSum = []
    index = 0
    for _ in range(round(len(shiftKeyingSamples)/SAMPLES_PER_BIT)):
        integralPerBitSum.append(productSamplesTrueOnly[index] - productSamplesFalseOnly[index])
        index += 1
        for _ in range(1, SAMPLES_PER_BIT):
            integralPerBitSum.append(integralPerBitSum[index - 1] + productSamplesTrueOnly[index] - productSamplesFalseOnly[index])
            index += 1
    demodulatedInformationSamples = [integral >= COMPARATOR_THRESHOLD for integral in integralPerBitSum]
    return integralPerBitSum, demodulatedInformationSamples

def drawScatter(x, y, title, ylabel, xlabel = 'Time'):
    plt.scatter(x, y, 1)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

def drawPlot(x, y, title, ylabel, xlabel = 'Time'):
    plt.plot(x, y, 1)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

def taskASKandPSK(time, informationSamples, informationSamplesTrueOnly, keyingFunction, shiftKeyingType):
    samples = keyingFunction(informationSamples, time)
    samplesTrueOnly = keyingFunction(informationSamplesTrueOnly, time)
    productSamples = [s * ts for s, ts in zip(samples, samplesTrueOnly)]
    integralPerBitSum, demodulatedInformationSamples = demodulationASKandPSK(samples, productSamples)

    plt.subplot(4, 1, 1)
    drawShiftKeyingPlot(time, informationSamples, samples, shiftKeyingType)

    plt.subplot(4, 1, 2)
    drawScatter(time, productSamples, "Product signal x(t)", "x(t)")

    plt.subplot(4, 1, 3)
    drawPlot(time, integralPerBitSum, "Integral per bit p(t)", "p(t)")

    plt.subplot(4, 1, 4)    
    drawPlot(time, demodulatedInformationSamples, "Demodulated signal m(t); H = " + str(COMPARATOR_THRESHOLD), "m(t)")

def taskFSK(time, informationSamples, informationSamplesTrueOnly, informationSamplesFalseOnly):
    samples = frequencyShiftKeying(informationSamples, time)
    samplesTrueOnly = frequencyShiftKeying(informationSamplesTrueOnly, time)
    samplesFalseOnly = frequencyShiftKeying(informationSamplesFalseOnly, time)

    productSamplesTrueOnly = [s * ts for s, ts in zip(samples, samplesTrueOnly)]
    productSamplesFalseOnly = [s * ts for s, ts in zip(samples, samplesFalseOnly)]

    integralPerBitSum, demodulatedInformationSamples = demodulationFSK(samples, productSamplesTrueOnly, productSamplesFalseOnly)

    plt.subplot(5, 1, 1)
    drawShiftKeyingPlot(time, informationSamples, samples, "Frequency")

    plt.subplot(5, 1, 2)
    drawScatter(time, productSamplesTrueOnly, "Product signal x1(t)", "x(t)")

    plt.subplot(5, 1, 3)
    drawScatter(time, productSamplesFalseOnly, "Product signal x2(t)", "x(t)")

    plt.subplot(5, 1, 4)
    drawPlot(time, integralPerBitSum, "Integral per bit p(t)", "p(t)")

    plt.subplot(5, 1, 5)
    drawPlot(time, demodulatedInformationSamples, "Demodulated signal m(t); H = " + str(COMPARATOR_THRESHOLD), "m(t)")

def task():
    FREQUENCY_MULTIPLIER = 1
    recalculateFrequencyConstants(FREQUENCY_MULTIPLIER)


    bits = stringToBinaryStream("Tak")
    time, informationSamples = informationSignal(SECONDS_PER_BIT, bits, SAMPLES_PER_BIT)
    _, informationSamplesTrueOnly = informationSignal(SECONDS_PER_BIT, tile(1, len(bits)), SAMPLES_PER_BIT)
    _, informationSamplesFalseOnly = informationSignal(SECONDS_PER_BIT, tile(0, len(bits)), SAMPLES_PER_BIT)

    plt.figure(figsize = (16, 9))
    taskASKandPSK(time, informationSamples, informationSamplesTrueOnly, amplitudeShiftKeying, "Amplitude")
    plt.tight_layout()
    plt.savefig("Charts/askDemodulation.png")

    plt.figure(figsize = (16, 9))
    taskASKandPSK(time, informationSamples, informationSamplesTrueOnly, phaseShiftKeying, "Phase")
    plt.tight_layout()
    plt.savefig("Charts/pskDemodulation.png")

    plt.figure(figsize = (16, 9))
    taskFSK(time, informationSamples, informationSamplesTrueOnly, informationSamplesFalseOnly)
    plt.tight_layout()
    plt.savefig("Charts/fskDemodulation.png")

    plt.show()


task()

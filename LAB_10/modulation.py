import matplotlib.pyplot as plt
import math as math
from utilities import string_to_binary_stream, linspace, tile

AMPLITUDE_LOW = 0
AMPLITUDE_HIGH = 1
PHASE_LOW = 0
PHASE_HIGH = math.pi
SECONDS_PER_BIT = 0.1
SAMPLES_PER_BIT = 1000
SAMPLING_FREQUENCY = int(SAMPLES_PER_BIT/SECONDS_PER_BIT)
FREQUENCY = 100/SECONDS_PER_BIT
FREQUENCY_LOW = FREQUENCY
FREQUENCY_HIGH = FREQUENCY_LOW * 2
COMPARATOR_THRESHOLD = 5

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

def demodulation_ask(shiftKeyingSamples):

    time, informationSamplesTrueOnly = informationSignal(SECONDS_PER_BIT, tile(1, int(len(shiftKeyingSamples) / SAMPLES_PER_BIT)), SAMPLES_PER_BIT)
    samplesTrueOnly = amplitudeShiftKeying(informationSamplesTrueOnly, time)
    productSamples = [s * ts for s, ts in zip(shiftKeyingSamples, samplesTrueOnly)]
    integralPerBitSum, demodulatedInformationSamples = demodulationASKandPSK(shiftKeyingSamples, productSamples)

    return convert_samples_to_bits(demodulatedInformationSamples)

def modulation_ask(bits):
    time, informationSamples = informationSignal(SECONDS_PER_BIT, bits, SAMPLES_PER_BIT)
    samples = amplitudeShiftKeying(informationSamples, time)
    return informationSamples, samples, time

def demodulation_psk(shiftKeyingSamples):

    time, informationSamplesTrueOnly = informationSignal(SECONDS_PER_BIT, tile(1, int(len(shiftKeyingSamples) / SAMPLES_PER_BIT)), SAMPLES_PER_BIT)
    samplesTrueOnly = phaseShiftKeying(informationSamplesTrueOnly, time)
    productSamples = [s * ts for s, ts in zip(shiftKeyingSamples, samplesTrueOnly)]
    integralPerBitSum, demodulatedInformationSamples = demodulationASKandPSK(shiftKeyingSamples, productSamples)

    return convert_samples_to_bits(demodulatedInformationSamples)

def modulation_psk(bits):
    time, informationSamples = informationSignal(SECONDS_PER_BIT, bits, SAMPLES_PER_BIT)
    samples = phaseShiftKeying(informationSamples, time)
    return informationSamples, samples, time

def demodulation_fsk(shiftKeyingSamples):

    time, informationSamplesTrueOnly = informationSignal(SECONDS_PER_BIT, tile(1, int(len(shiftKeyingSamples) / SAMPLES_PER_BIT)), SAMPLES_PER_BIT)
    _, informationSamplesFalseOnly = informationSignal(SECONDS_PER_BIT, tile(0, int(len(shiftKeyingSamples) / SAMPLES_PER_BIT)), SAMPLES_PER_BIT)

    samplesTrueOnly = frequencyShiftKeying(informationSamplesTrueOnly, time)
    samplesFalseOnly = frequencyShiftKeying(informationSamplesFalseOnly, time)

    productSamplesTrueOnly = [s * ts for s, ts in zip(shiftKeyingSamples, samplesTrueOnly)]
    productSamplesFalseOnly = [s * ts for s, ts in zip(shiftKeyingSamples, samplesFalseOnly)]

    integralPerBitSum, demodulatedInformationSamples = demodulationFSK(shiftKeyingSamples, productSamplesTrueOnly, productSamplesFalseOnly)

    return convert_samples_to_bits(demodulatedInformationSamples)

def modulation_fsk(bits):
    time, informationSamples = informationSignal(SECONDS_PER_BIT, bits, SAMPLES_PER_BIT)
    samples = frequencyShiftKeying(informationSamples, time)
    return informationSamples, samples, time

def modulate(bits, modulation_type):
    method = None
    if (modulation_type == 'ask'):
        method = modulation_ask
    elif (modulation_type == 'psk'):
        method = modulation_psk
    elif (modulation_type == 'fsk'):
        method = modulation_fsk
    return method(bits)

def demodulate(shift_keying_samples, modulation_type):
    method = None
    if (modulation_type == 'ask'):
        method = demodulation_ask
    elif (modulation_type == 'psk'):
        method = demodulation_psk
    elif (modulation_type == 'fsk'):
        method = demodulation_fsk
    return method(shift_keying_samples)

def convert_samples_to_bits(samples):
    bits = []
    for i in range(round(len(samples)/SAMPLES_PER_BIT)):
        index = i * SAMPLES_PER_BIT
        bit_sum = sum(samples[index:(index + SAMPLES_PER_BIT)])
        bits.append(bool(bit_sum > SAMPLES_PER_BIT / 2))
    return bits

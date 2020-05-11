import matplotlib.pyplot as plt
import math as math
from math import ceil

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
    return [value for _ in range(int(count))]

#recreates numpy linspace
def linspace(low, high, stepCount):
    step = (high - low) / (stepCount - 1)
    values = [low + step * i for i in range(stepCount)]
    return values

SECONDS_PER_BIT = 0.1
SAMPLES_PER_BIT = 100

def generateClockSignal(samplesPerBit, clockCount):
    halfSamples = int(samplesPerBit / 2)

    clockSamples = samplesPerBit * clockCount * [None]
    for i in range(clockCount * 2):
        clockSamples[i * halfSamples:(i + 1) * halfSamples] = tile((i % 2) == 0, halfSamples)
    return clockSamples

def informationSignal(secondsPerBit, bits, samplesPerBit):
    time = linspace(0, secondsPerBit * len(bits), samplesPerBit * len(bits))

    signalSamples = samplesPerBit * len(bits) * [None]
    for i, bit in enumerate(bits):
        signalSamples[i * samplesPerBit:(i + 1) * samplesPerBit] = tile(bit, samplesPerBit)
    return time, signalSamples

NRZI_START = -1
def nrziCoder(clk, ttl):
    nrzi = [0]
    currentValue = 0
    for i in range(len(clk) - 1):
        if (clk[i] == 1 and clk[i + 1] == 0): #wzgórze malejące
            if currentValue == 0:
                currentValue = NRZI_START
            else:
                if (ttl[i]):
                    currentValue *= -1
        nrzi.append(currentValue)
    return nrzi

def bamiCoder(clk, ttl):
    nrzi = [0]
    currentValue = 0
    highValue = -1
    for i in range(len(clk) - 1):
        if (clk[i] == 0 and clk[i + 1] == 1): #wzgórze narastające
            if (ttl[i + 1]):
                currentValue = highValue
                highValue *= -1
            else:
                currentValue = 0
        nrzi.append(currentValue)
    return nrzi

def manchesterCoder(clk, ttl):
    nrzi = [0]
    currentValue = 0

    for i in range(len(clk) - 1):
        if (clk[i] == 1 and clk[i + 1] == 0): #wzgórze malejące
            if (ttl[i] == 0):
                currentValue = 1
            else:
                currentValue = -1
        elif (clk[i] == 0 and clk[i + 1] == 1): #wzgórze narastające
            if (ttl[i] == ttl[i + 1]):
                currentValue *= -1
        nrzi.append(currentValue)
    return nrzi

def bamiDecoder(bami):
    return [not (sample == 0) for sample in bami]

def nrziDecoder(nrzi, samplesPerbit, secondsPerBit):
    nrziTrueFalse = [sample == 1 for sample in nrzi]
    ttl = []
    time = linspace(secondsPerBit / 2, (len(nrzi) / samplesPerbit) * secondsPerBit - secondsPerBit / 2, len(nrzi) - samplesPerbit)
    for i in range(int(samplesPerbit), len(nrzi)):
        ttl.append(nrziTrueFalse[i - samplesPerbit] ^ nrziTrueFalse[i])
    return time, ttl

def ttlToBits(ttl, samplesPerBit):
    bits = []
    for i in range(0, ceil(len(ttl) / samplesPerBit)):
        bits.append(ttl[i * samplesPerBit])
    return bits

def manchesterDecoder(clock, manchester, samplesPerbit):
    quarterSamplesPerBit = int(samplesPerbit / 4)
    clock = tile(1, quarterSamplesPerBit) + clock
    clock = clock[:int(len(clock) - quarterSamplesPerBit)]

    bits = []
    for i in range(len(clock) - 1):
        if (clock[i] == 1 and clock[i + 1] == 0): #wzgórze malejące
            bits.append(manchester[i])
    return bits
   
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

def plotSignal(time, samples, subplot, yLabel, color = 'b', xLimLeft = 0, xLimRight = None):
    if xLimRight is None:
        xLimRight = max(time)
    ax = plt.subplot(8, 1, subplot)
    ax.axhline(0, linestyle='--', c='k', alpha = 0.5)
    ax.plot(time, samples, color, label = yLabel)
    ax.set_ylabel(yLabel)
    ax.set_xlim(xLimLeft, xLimRight)
    plt.legend()

def task(bits, filename):
    clk = generateClockSignal(SAMPLES_PER_BIT, len(bits))
    t, ttl = informationSignal(SECONDS_PER_BIT, bits, SAMPLES_PER_BIT)

    nrziSamples = nrziCoder(clk, ttl)
    timeNrzi, ttlNrzi = nrziDecoder(nrziSamples, SAMPLES_PER_BIT, SECONDS_PER_BIT)
    nrziBits = ttlToBits(tile(False, SAMPLES_PER_BIT / 2) + ttlNrzi, SAMPLES_PER_BIT)

    bamiSamples = bamiCoder(clk, ttl)
    ttlBami = bamiDecoder(bamiSamples)
    bamiBits = ttlToBits(ttlBami, SAMPLES_PER_BIT)

    manchesterSamples = manchesterCoder(clk, ttl)
    manchesterBits = manchesterDecoder(clk, ttl, SAMPLES_PER_BIT)
    tzz, manchestersTtl = informationSignal(SECONDS_PER_BIT, manchesterBits, SAMPLES_PER_BIT)

    plt.figure(figsize=(16, 9))
    plotSignal(t, clk, 1, 'CLK', 'k')
    plotSignal(t, ttl, 2, 'TTL', 'c')
    plotSignal(t, nrziSamples, 3, 'NRZI', 'k')
    plotSignal(timeNrzi, ttlNrzi, 4, 'NRZI TTL', 'k', xLimRight=max(t))
    plotSignal(t, bamiSamples, 5, 'BAMI', 'purple')
    plotSignal(t, ttlBami, 6, 'BAMI TTL', 'purple')
    plotSignal(t, manchesterSamples, 7, 'Manchester', 'g')
    plotSignal(tzz, manchestersTtl, 8, 'Manchester TTL', 'g')

    #First bit is lost in nrzi & bami and last bit in menchester
    print(bits)
    print(nrziBits)
    print(bamiBits)
    print(manchesterBits)
    plt.tight_layout()
    plt.savefig('Charts/' + filename)

bits = [1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0]
takBits = stringToBinaryStream('Tak')
task(bits, 'fromSite.png')
task(takBits[0:16], 'Tak.png')
plt.show()

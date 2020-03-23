import matplotlib.pyplot as plt
import numpy as np
import math

def loadFile(filename):
    return np.loadtxt('Outputs/' + filename + '.csv', delimiter=',', unpack=True, skiprows = 1)

def filterNoise(filename, filterParameter):
    frequencies, amplitudes = loadFile(filename)
    frequenciesFiltered = []
    amplitudesFiltered = []
    minimumAmplitude = max(amplitudes) / filterParameter
    for i, amplitude in enumerate(amplitudes):
        if (amplitude > minimumAmplitude):
            amplitudesFiltered.append(amplitude)
            frequenciesFiltered.append(frequencies[i])
    return amplitudesFiltered, frequenciesFiltered

def convertToDecibelScale(amplitudes):
    amplitudesAsDecibels = []
    for i, amplitude in enumerate(amplitudes):
        amplitudesAsDecibels.append(math.log10(amplitude) * 10)
    return amplitudesAsDecibels

def drawPlot(functionName, title, filename):
    t, y = np.loadtxt('Outputs/' + filename + '.csv', delimiter=',', unpack=True, skiprows = 1)
    plt.scatter(t, y, 1, color='tab:blue')
    plt.title('Plot of ' + title)
    plt.xlabel('t')
    plt.ylabel(functionName + '(t)')
    plt.grid(axis='y')

def drawFrequencyPlot(x, y, title, filename):
    plt.stem(x, y, markerfmt = 'C1o')
    plt.title('Plot of ' + title)
    plt.xlabel('Frequency')
    plt.ylabel('Ampltiude')
    plt.grid(axis='y')

def secondTask():
    plt.figure(figsize = (16, 9))
    amplitudes, frequencies = filterNoise('sAmplitudes', 100)
    amplitudesDecimal = convertToDecibelScale(amplitudes)
    plt.subplot(1, 3, 1)
    drawPlot(*('s', 's(t)', 's'))
    plt.subplot(1, 3, 2)
    drawFrequencyPlot(frequencies, amplitudes, 'dft(s(t))', 'sAmplitudes')
    plt.subplot(1, 3, 3)
    drawFrequencyPlot(frequencies, amplitudesDecimal, 'toDecibelScale(dft(s(t)))', 'sDecibel')
    plt.savefig('Charts/secondTask.png', dpi = 200)

def thirdTaskPartOne():

    files = ('x', 'y', 'v', 'z', 'u')
    for i, file in enumerate(files):
        plt.figure(figsize = (12, 9))
        amplitudes, frequencies = filterNoise(file + 'Amplitudes', 25)
        amplitudesDecimal = convertToDecibelScale(amplitudes)
        plt.subplot(1, 2, 1)
        drawPlot(*(file, file + '(t)', file))
        plt.subplot(1, 2, 2)
        drawFrequencyPlot(frequencies, amplitudesDecimal, 'toDecibelScale(dft(' + file + '(t)))', 'sAmplitudes')
        plt.savefig('Charts/' + file + 'ThirdTask.png', dpi = 150)

def thirdTaskPartTwo():
    plt.figure(figsize = (16, 9))
    files = ('p2', 'p4', 'pAB')
    for i, file in enumerate(files):
        amplitudes, frequencies = filterNoise(file + 'Amplitudes', 25)
        amplitudesDecimal = convertToDecibelScale(amplitudes)
        plt.subplot(3, 2, i * 2 + 1)
        drawPlot(*(file, file + '(t)', file))
        plt.subplot(3, 2, i * 2 + 2)
        drawFrequencyPlot(frequencies, amplitudesDecimal, 'toDecibelScale(dft(' + file + '(t)))', 'sAmplitudes')
    plt.tight_layout()
    plt.savefig('Charts/pThirdTask.png', dpi = 150)

def fourthTask():
    plt.figure(figsize = (16, 9))
    amplitudes, frequencies = filterNoise('sAmplitudes', 100)
    amplitudesDecimal = convertToDecibelScale(amplitudes)
    plt.subplot(1, 3, 1)
    drawPlot(*('s', 's(t)', 's'))
    plt.subplot(1, 3, 2)
    drawFrequencyPlot(frequencies, amplitudesDecimal, 'toDecibelScale(dft(s(t)))', 'sDecibel')
    plt.subplot(1, 3, 3)
    drawPlot(*('s', 's(t) after DFT and IDFT', 'sReversed'))
    plt.savefig('Charts/fourthTask.png', dpi = 200)

secondTask()
thirdTaskPartOne()
thirdTaskPartTwo()
fourthTask()
#plt.show()
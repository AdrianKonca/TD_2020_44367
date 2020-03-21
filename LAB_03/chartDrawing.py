import matplotlib.pyplot as plt
import numpy as np

functions = (('s', 's(t)', 's'), ('s', 'Quantized s(t) for q = 16', 'sQuantized'), ('s','Quantized s(t) for q = 8', 'sQuantizedHalf'))
decimation = 1

def drawPlot(functionName, title, filename):
    t, y = np.loadtxt('Outputs/' + filename + '.csv', delimiter=',', unpack=True, skiprows = 1)
    plt.clf()

    plt.scatter(t[::decimation], y[::decimation], 1, color='tab:blue', )
    plt.title('Plot of ' + title)
    plt.xlabel('t')
    plt.ylabel(functionName + '(t)')
    plt.grid(axis='y')
    plt.savefig('Charts/' + filename + '.png', dpi=200)

for i, function in enumerate(functions):
    drawPlot(function[0], function[1], function[2])

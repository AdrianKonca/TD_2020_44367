import matplotlib.pyplot as plt
import numpy as np

functionNames = ('x', 'y', 'z', 'u', 'v', 'p2', 'p4', 'pAB')

def drawPlot(functionName):
    t, y = np.loadtxt('Outputs/' + functionName + '.csv', delimiter=',', unpack=True, skiprows = 1)
    plt.clf()
    plt.plot(t, y, color='tab:blue')
    plt.title('Plot of ' + functionName + '(t) function')
    plt.xlabel('t')
    plt.ylabel('y')
    plt.grid(axis='y')
    plt.savefig('Charts/' + functionName + '.png', dpi=200)

for i, functionName in enumerate(functionNames):
    drawPlot(functionName)

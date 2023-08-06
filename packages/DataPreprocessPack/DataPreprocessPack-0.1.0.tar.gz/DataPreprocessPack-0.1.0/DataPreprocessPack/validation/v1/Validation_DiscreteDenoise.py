import numpy as np
import matplotlib.pyplot as plt

from DataPreprocessPack.toolbox.v1.Method_DiscreteDenoise import DiscreteDenoise


def main():
    quant = 5000
    start = -7
    end = 7
    data = np.sin(np.arange(start, end, (end-start)/quant)) * 2
    noise = np.random.rand(quant)
    wave = data+noise

    bufferCache = []
    smoothed = []
    for i in range(quant):
        obj = DiscreteDenoise(windowSize=50, buffer=bufferCache, func=np.max)
        obj.smooth(wave[i])
        bufferCache = obj._buffer
        smoothed.append(obj.output)

    plt.plot(wave, label="wave")
    plt.plot(smoothed, label="smooth")
    plt.legend()
    plt.show()
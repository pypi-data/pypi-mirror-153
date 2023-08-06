import pandas as pd
import numpy as np

from DataPreprocessPack.toolbox.v1.Method_NanFill import NanFill

def main():
    quant = 10000
    nanPercentage = 0.7
    data = pd.DataFrame({"value": np.random.rand(1, quant).flatten().tolist()})
    _randomNanLocs = pd.DataFrame({"loc": np.arange(quant)}).sample(int(quant * nanPercentage))
    dataWithNan = data.copy()
    dataWithNan.loc[_randomNanLocs["loc"], ["value"]] = np.nan
    dataWithNan = dataWithNan.values.flatten().tolist()
    print(dataWithNan)
    bufferInit = []
    nanCountInit = 0
    for i in range(quant):
        _newValue = dataWithNan[i]
        # nanFillObj = NanFill(buffer=bufferInit, bufferSize=20, nanCount=nanCountInit, nanToleranceQuant=3, method="measured")
        # nanFillObj = NanFill(buffer=bufferInit, bufferSize=20, nanCount=nanCountInit, nanToleranceQuant=3, method="average")
        # nanFillObj = NanFill(buffer=bufferInit, bufferSize=20, nanCount=nanCountInit, nanToleranceQuant=3, method="max")
        nanFillObj = NanFill(buffer=bufferInit, bufferSize=20, nanCount=nanCountInit, nanToleranceQuant=3, method="min")
        nanFillObj.update(_newValue)
        bufferInit = nanFillObj._buffer
        nanCountInit = nanFillObj._nanCount
        _cache = pd.DataFrame({"cache": nanFillObj._buffer}).dropna().min()
        print("原始值：", _newValue, "\t补值：", nanFillObj.processedValue, "\t当前缓存：", len(nanFillObj._buffer), _cache, nanFillObj._buffer, "\n", "="*20)

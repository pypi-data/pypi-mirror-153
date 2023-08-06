import pandas as pd
import numpy as np


class NanFill:
    """
    根据输入的单点数据,对np.nan数据进行补值
     - 可以选择多种补值方式(如:最近实测值measured、近期最大值max、近期最小值min、近期均值average),但不可选择方向(默认前序补值"ffill"的方式)
     - 当连续出现np.nan值且超过允许的数量(nanToleranceQuant)时,停止补值(仍然进行补值计算,但输出为nan)
     - 计算近期最值和均值的依据,是类属性_buffer中的单点数据缓存
     - 数据缓存尺寸通过bufferSize控制

    注意:
     - 属性_buffer和_nanCount在IOT平台中可能需要显性缓存


    [1] 参数
    ----------
    _buffer:
        list, 数据缓存, 默认[]
    _bufferSize:
        int, 数据缓存数量, 默认50
    _nanCount:
        int, 连续出现的np.nan数量, 默认0
    method:
        str, 出现np.nan时的补值方法, 无缺省值, 必须指定
    nanToleranceQuant:
        int, 允许连续出现np.nan的次数, 默认10
    processedValue:
        float, 当期补值

    [2] 方法
    ----------
    update:
        输入本次实测数据,允许为np.nan

    [3] 返回
    -------
    processedValue:
        float, 当期补值

    _buffer:
        list, 数据缓存

    _nanCount:
        int, 连续出现的np.nan数量

    [4] 示例1
    --------
    >>> quant = 10000
    >>> nanPercentage = 0.7
    >>> data = pd.DataFrame({"value": np.random.rand(1, quant).flatten().tolist()})
    >>> _randomNanLocs = pd.DataFrame({"loc": np.arange(quant)}).sample(int(quant * nanPercentage))
    >>> dataWithNan = data.copy()
    >>> dataWithNan.loc[_randomNanLocs["loc"], ["value"]] = np.nan
    >>> dataWithNan = dataWithNan.values.flatten().tolist()
    >>> bufferInit = []
    >>> nanCountInit = 0
    >>> for i in range(quant):
    >>>     _newValue = dataWithNan[i]
    >>>     # nanFillObj = NanFill(buffer=bufferInit, bufferSize=20, nanCount=nanCountInit, nanToleranceQuant=3, method="measured")
    >>>     # nanFillObj = NanFill(buffer=bufferInit, bufferSize=20, nanCount=nanCountInit, nanToleranceQuant=3, method="average")
    >>>     # nanFillObj = NanFill(buffer=bufferInit, bufferSize=20, nanCount=nanCountInit, nanToleranceQuant=3, method="max")
    >>>     nanFillObj = NanFill(buffer=bufferInit, bufferSize=20, nanCount=nanCountInit, nanToleranceQuant=3, method="min")
    >>>     nanFillObj.update(_newValue)
    >>>     bufferInit = nanFillObj._buffer
    >>>     nanCountInit = nanFillObj._nanCount
    >>>     _cache = pd.DataFrame({"cache": nanFillObj._buffer}).dropna().min()
    >>>     print('原始值：', _newValue, '补值：', nanFillObj.processedValue, '\t当前缓存：', len(nanFillObj._buffer), _cache, nanFillObj._buffer)
    """
    def __init__(self, method: str ="measured", nanToleranceQuant: int=10, **kwargs):
        self._buffer = kwargs["buffer"] if "buffer" in kwargs.keys() else []  # 数据缓存
        self._bufferSize = kwargs["bufferSize"] if "bufferSize" in kwargs.keys() else 50  # 数据缓存尺寸限制
        self._nanCount = kwargs["nanCount"] if "nanCount" in kwargs.keys() else 0  # 数据缓存尺寸限制
        self.method = method
        self.nanToleranceQuant = nanToleranceQuant
        self.processedValue = None

        # 检查/更新buffer尺寸
        while len(self._buffer) >= self._bufferSize:
            self._buffer.pop(0)

    def update(self, newValue: float):
        """
        根据输入的数据进行补值

        :param newValue: 当期实测值
        :param type: float
        """
        self._buffer.append(newValue)
        if np.isnan(newValue):
            self._nanCount+=1
            if self.__NanQuantOverLimit():
                self.processedValue = np.nan
            else:
                self.processedValue = self.__NanFill()

        else:
            self._nanCount = 0
            self.processedValue = newValue

    def __NanQuantOverLimit(self):
        if self._nanCount <= self.nanToleranceQuant:
            return False
        else:
            return True

    def __NanFillWithMeasured(self, _buffer: pd.DataFrame):
        return _buffer.fillna(axis=0, method="ffill")

    def __NanFillWithAverage(self, _buffer: pd.DataFrame):
        return _buffer.fillna(axis=0, value=_buffer.dropna(axis=0).mean().values.flatten().tolist()[0])

    def __NanFillWithMax(self, _buffer: pd.DataFrame):
        return _buffer.fillna(axis=0, value=_buffer.dropna(axis=0).max().values.flatten().tolist()[0])

    def __NanFillWithMin(self, _buffer: pd.DataFrame):
        return _buffer.fillna(axis=0, value=_buffer.dropna(axis=0).min().values.flatten().tolist()[0])


    def __NanFill(self):
        _buffer = pd.DataFrame({"values": self._buffer})
        _nanFillMethods = {
            "measured": self.__NanFillWithMeasured,
            "average": self.__NanFillWithAverage,
            "max": self.__NanFillWithMax,
            "min": self.__NanFillWithMin
        }
        _buffer = _nanFillMethods[self.method](_buffer)
        self._buffer[-1] = _buffer.iloc[-1, 0]
        return _buffer.iloc[-1, 0]
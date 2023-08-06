import numpy as np


class DiscreteDenoise:
    """
    对离散型单变量数据进行降噪, 通过近期的数据缓存情况计算一阶差分的分布情况(默认该变量为高信噪比信号), 当新传入数据的一阶差分突破允许范围时
    使用最近数期数据经某种计算(如:部分缓存数据的均值average、最值max min、分位值1st 3rd, 或使用func自定义函数)后代替该值

    注意:
     - 属性_buffer在IOT平台中可能需要显性缓存

    [1] 参数
    ----------
    buffer:
        list, 数据缓存, 默认[]
    bufferSize:
        int, 数据缓存的尺寸, 默认为windowSize的5倍
    windowSize:
        int, 当缓存中的数据量达到此值时, 开始输出降噪后的值, 默认200
    batchWindowSize:
        int, 满足降噪数据计算条件时, 使用缓存中最近的数据(个数为batchWindowSize)作为输入 开始输出降噪后的值, 默认50
    coef:
        float, 当新传入值的前序值的一阶差分在缓存数据所指的噪声分布的允许值(mean ± coef * sigma)之外时, 当期需要输出降噪后的值, 默认10e-5
    func:
        function, 降噪的计算方法, 该计算方法的输入是缓存中最近的数据(个数为batchWindowSize)

    [2] 方法
    ----------
    smooth:
        根据输入的newValue及前序的缓存, 对数据进行降噪处理

    [3] 返回
    -------
    output:
        若满足降噪条件, 则为降噪后的值, 否则为原始的输入值

    [4] 示例1
    --------
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> quant = 5000
    >>> start = -7
    >>> end = 7
    >>> data = np.sin(np.arange(start, end, (end-start)/quant)) * 2
    >>> noise = np.random.rand(quant)
    >>> wave = data+noise
    >>> bufferCache = []
    >>> smoothed = []
    >>> for i in range(quant):
    >>>     obj = DiscreteDenoise(windowSize=50, buffer=bufferCache, func=np.max)
    >>>     obj.smooth(wave[i])
    >>>     bufferCache = obj._buffer
    >>>     smoothed.append(obj.output)
    >>>
    >>> plt.plot(wave, label="wave")
    >>> plt.plot(smoothed, label="smooth")
    >>> plt.legend()
    >>> plt.show()
    """
    def __init__(self, windowSize=200, method="average", **kwargs):
        self.windowSize = windowSize
        self.method = method
        self._buffer = kwargs["buffer"] if len(kwargs["buffer"]) > 0 else []
        self._bufferSize = kwargs["bufferSize"] if "bufferSize" in kwargs.keys() else int(windowSize*5)
        while len(self._buffer) >= self._bufferSize:self._buffer.pop(0)
        self.output = None
        self.coef = kwargs["coef"] if "coef" in kwargs.keys() else 10e-5
        self.batchWindowSize = kwargs["batchWindowSize"] if "batchWindowSize" in kwargs.keys() else 50
        self.func = kwargs["func"] if "func" in kwargs.keys() else None
        if self.func: self.method = "func"


    def smooth(self, newValue: float):
        """
        判断当期输入值是否需要进行降噪, 并输出相应的值

        :param newValue: 当期实测值
        :type newValue: float
        :return: None
        """
        if len(self._buffer) >= self.windowSize:
            _sig, _mean = np.std(np.diff(self._buffer)), np.mean(np.diff(self._buffer))
            if ((newValue - self._buffer[-1]) > _mean + self.coef*_sig) or ((newValue - self._buffer[-1]) < _mean - self.coef*_sig):
                processedValue = self.__process()
            else:
                processedValue = newValue
        else:
            processedValue = newValue
        self._buffer.append(newValue)
        self.output = processedValue

    def __process(self):
        _methods = {
            "average": np.average, "max": np.max, "min": np.min,
            "1st": lambda x: np.quantile(x, 0.25), "3rd": lambda x: np.quantile(x, 0.75),
        }
        if self.func:
            return self.func(self._buffer[-self.batchWindowSize:])
        else:
            return _methods[self.method](self._buffer[-self.batchWindowSize:])
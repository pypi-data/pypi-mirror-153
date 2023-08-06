import pandas as pd
import numpy as np
import datetime


class TimestampAlign:
    """
    多个散点型测点的对齐
    - 适用于相同频率的散点型数据的时间戳对齐
    - 可以使用多种时间戳选择方式（如：用前序forward的时间戳/最远的时间,用后序backward的时间戳/最近的时间,用均值average的时间戳/最均衡的时间)
    - 要求每个时间序列的时间戳均应为相同的column名,默认ts
    - 每个时间序列的长度均应为 1

    [1] 参数
    ----------
    method:
        str, 使用何种方法对将多个时间戳转换为单个时间戳,默认forward
    tsSign:
        str, 所有输入的时间序列的column名, 默认ts

    [2] 方法
    ----------
    align:
        输入多个时间序列, 对齐后输出
        - 要求输入的每个时间序列的column形如["ts", "value1"]、["ts", "value2"], 长度为 1

    [3] 返回
    -------
    output:
        dataframe, 经过对齐后的时间序列, column名为["value1", "value2"], index为时间戳, 长度为 1

    [4] 示例1
    --------
    >>>    quant = 10000
    >>>    nanPercentage = 0.7
    >>>    values1 = pd.DataFrame({"value1": np.random.rand(1, quant).flatten().tolist()})
    >>>    times1 = pd.date_range("2022-06-01 00:00:00.000010", freq="1S", periods=quant).to_frame(name="ts").reset_index(drop=True)
    >>>    values2 = pd.DataFrame({"value2": np.random.rand(1, int(quant*2)).flatten().tolist()})
    >>>    times2 = pd.date_range("2022-06-01 00:00:00.013000", freq="0.5S", periods=int(quant*2)).to_frame(name="ts").reset_index(drop=True)
    >>>    values3 = pd.DataFrame({"value3": np.random.rand(1, int(quant*2/5)).flatten().tolist()})
    >>>    times3 = pd.date_range("2022-06-01 00:00:00.013000", freq="2.5S", periods=int(quant*2/5)).to_frame(name="ts").reset_index(drop=True)
    >>>    df1 = pd.concat([times1, values1], axis=1, ignore_index=True); df1.columns = ["ts", "value1"]
    >>>    # df1["ts"] = df1.apply(lambda x: datetime.datetime.timestamp(x["ts"]), axis=1)
    >>>    df2 = pd.concat([times2, values2], axis=1, ignore_index=True); df2.columns = ["ts", "value2"]
    >>>    # df2["ts"] = df2.apply(lambda x: datetime.datetime.timestamp(x["ts"]), axis=1)
    >>>    df3 = pd.concat([times3, values3], axis=1, ignore_index=True); df3.columns = ["ts", "value3"]
    >>>    # df3["ts"] = df3.apply(lambda x: datetime.datetime.timestamp(x["ts"]), axis=1)
    >>>
    >>>    obj = TimestampAlign(method="backward")
    >>>    recorder = pd.DataFrame()
    >>>    for i in range(int(quant*2/5)):
    >>>        obj.align(value1=df1.iloc[i, :], value2=df2.iloc[i, :])
    >>>        if len(recorder) == 0:
    >>>            recorder = obj.output
    >>>        else:
    >>>            recorder = recorder.append(obj.output)
    >>>    print(recorder)
    """
    def __init__(self, method="forward", tsSign="ts"):
        self.method = method
        self.tsSign = tsSign
        self.output = None
        self.uniqueTime = None

    def align(self, **kwargs):
        self.output = self.__concat(**kwargs)

    def __concat(self, **kwargs):
        _times = [kwargs[item][self.tsSign] for item in kwargs.keys()]
        _values = [kwargs[item].drop(self.tsSign).values.flatten().tolist()[0] for item in kwargs.keys()]
        _names = [kwargs[item].drop(self.tsSign).index[0] for item in kwargs.keys()]
        if self.method == "forward":
            self.uniqueTime = min(_times)
        elif self.method == "average":
            self.uniqueTime = np.average(_times)
        else:
            self.uniqueTime = max(_times)
        _dict = {}
        for i in range(len(_values)):
            _dictCache = {_names[i]: {self.uniqueTime: _values[i]}}
            _dict = {**_dict, **_dictCache}
        return pd.DataFrame(_dict)
import pandas as pd
import numpy as np
import datetime

from DataPreprocessPack.toolbox.v1.Method_TimestampAlign import TimestampAlign

def main():
    quant = 1000
    nanPercentage = 0.7
    values1 = pd.DataFrame({"value1": np.random.rand(1, quant).flatten().tolist()})
    times1 = pd.date_range("2022-06-01 00:00:00.000010", freq="1S", periods=quant).to_frame(name="ts").reset_index(drop=True)
    values2 = pd.DataFrame({"value2": np.random.rand(1, int(quant*2)).flatten().tolist()})
    times2 = pd.date_range("2022-06-01 00:00:00.013000", freq="0.5S", periods=int(quant*2)).to_frame(name="ts").reset_index(drop=True)
    values3 = pd.DataFrame({"value3": np.random.rand(1, int(quant*2/5)).flatten().tolist()})
    times3 = pd.date_range("2022-06-01 00:00:00.013000", freq="2.5S", periods=int(quant*2/5)).to_frame(name="ts").reset_index(drop=True)

    df1 = pd.concat([times1, values1], axis=1, ignore_index=True); df1.columns = ["ts", "value1"]
    # df1["ts"] = df1.apply(lambda x: datetime.datetime.timestamp(x["ts"]), axis=1)
    df2 = pd.concat([times2, values2], axis=1, ignore_index=True); df2.columns = ["ts", "value2"]
    # df2["ts"] = df2.apply(lambda x: datetime.datetime.timestamp(x["ts"]), axis=1)
    df3 = pd.concat([times3, values3], axis=1, ignore_index=True); df3.columns = ["ts", "value3"]
    # df3["ts"] = df3.apply(lambda x: datetime.datetime.timestamp(x["ts"]), axis=1)

    obj = TimestampAlign(method="backward")
    recorder = pd.DataFrame()
    for i in range(int(quant*2/5)):
        obj.align(value1=df1.iloc[i, :], value2=df2.iloc[i, :])
        if len(recorder) == 0:
            recorder = obj.output
        else:
            recorder = recorder.append(obj.output)
    print(recorder)

import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

def spikecount(series):
    """
    Counts the amount of spikes in a series
    """
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return len(series[series > q3 + 1.5 * iqr])
def sub5freq(series):
    return int(100*len(series[series < 5])/len(series))
def hyp10freq(series):
    return int(100*len(series[series > 10])/len(series))


def main():
    #loads the dataframe
    OGdf = pd.read_csv("./log.csv")
    #filters out rows that are recording during charging, because the W reading is off in these cases
    df = OGdf[OGdf["charging"] == 0]
    df = df.copy()
    df["session"] = df["session"].fillna("No process")
    #allows to unify each combo of applications into a tuple
    # df["session_list"] = df["session"].fillna(" ").str.split("+").apply(sorted)
    # df["session_tuple"] = df["session_list"].apply(tuple)
    #filters out combos with less than 5 entries
    counts = df["session"].value_counts()
    df = df[df["session"].isin(counts[counts >= 5].index)]

    df["hour"] = pd.to_datetime(df["time"], format="%H:%M").dt.hour
    #calculates stats such as average, median etc...
    cs = df.groupby("session")["power"].agg(["count", "mean", "median", "std", spikecount, sub5freq, hyp10freq]).reset_index()
    print(cs)

    #graphing
    plt.bar(cs["session"], cs["median"])
    plt.xlabel("session combo")
    plt.ylabel("median power consumption")
    plt.title(f"median power consumption per session combo")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.bar(cs["session"], cs["sub5freq"])
    plt.xlabel("session combo")
    plt.ylabel("under 5W usage frequency")
    plt.title(f"under 5W usage frequency per session combo")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    plt.bar(cs["session"], cs["hyp10freq"])
    plt.xlabel("session combo")
    plt.ylabel("over 10W usage frequency")
    plt.title(f"over 10W usage frequency per session combo")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    hrmdn = df.groupby("hour")["power"].median()
    plt.bar(hrmdn.index, hrmdn.values)
    plt.xlabel("time")
    plt.ylabel("median power consumption")
    plt.title(f"median poewr consumption throughout the day")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

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

    GRAPHS = ["mdnpwr/sesh", "sub5/sesh","hyp10/sesh","spkfr/sesh","draw/time"]
    graph_params = {
            "mdnpwr/sesh": {
                "x":cs["session"],
                "y":cs["median"],
                "xlabel":"session combo",
                "ylabel":"median power consumption",
                "title":"median power consumption per session combo"
            },
            "sub5/sesh": {
                "x":cs["session"],
                "y":cs["sub5freq"],
                "xlabel":"session combo",
                "ylabel":"under 5W draw frequency",
                "title":"under 5W draw frequency per session combo"
            },
            "hyp10/sesh": {
                "x":cs["session"],
                "y":cs["hyp10freq"],
                "xlabel":"session combo",
                "ylabel":"over 10W draw frequency",
                "title":"over 10W draw frequency per session combo"
            },
            "spkfr/sesh": {
                "var":100*cs["spikecount"]/cs["count"],
                "x":cs["session"],
                "y":100*cs["spikecount"]/cs["count"],
                "xlabel":"session combo",
                "ylabel":"spike frequency",
                "title":"spike frequency per session combo"
            },
            "draw/time": {
                "var":df.groupby("hour")["power"].median(),
                "x":df.groupby("hour")["power"].median().index,
                "y":df.groupby("hour")["power"].median().values,
                "xlabel":"time",
                "ylabel":"median power consumption",
                "title":"median power consumption throughout the day"
            },
            }
    for graph in GRAPHS:
        pars = graph_params[graph]
        plt.bar(pars["x"], pars["y"])
        plt.xlabel(pars["xlabel"])
        plt.ylabel(pars["ylabel"])
        plt.title(pars["title"])
        plt.grid(True)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()

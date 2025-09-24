import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt


def main():
    pcs = ["ollama", "sway", "plasma"]
    OGdf = pd.read_csv("./log.csv")
    dc_df = OGdf[OGdf["charging"] == 0]
    dc_df = dc_df.copy()
    dc_df["session_list"] = dc_df["session"].fillna(" ").str.split("+").apply(sorted)
    dc_df["session_tuple"] = dc_df["session_list"].apply(tuple)
    results = {}
    for combo, df in dc_df.groupby("session_tuple"):
        smp_sz = len(df)
        if smp_sz < 5:
            continue
        comboname = df["session"].iloc[1]
        pwr = df["power"]
        # simple calculations
        mean = pwr.mean()
        mdn = pwr.median()
        std = pwr.std()
        q1 = pwr.quantile(0.25)
        q3 = pwr.quantile(0.75)
        iqr = q3 - q1
        spks = len(df[pwr > q3 + 1.5 * iqr])
        spkfreq = int(100 * spks / smp_sz)
        sub5freq = int((len(df[df["power"] < 5]) / smp_sz) * 100)
        hyp10freq = int((len(df[df["power"] > 10]) / smp_sz) * 100)
        print(
            f"for combo: {comboname},\nsample size: {smp_sz}\nmean: {mean},\nmedian:{mdn}\nstandard deviation:{std}\nAmount of spikes: {spks}({spkfreq}%) \nsub5W frequency: {sub5freq}%\nover 10W frequency: {hyp10freq}%\n"
        )
        results[comboname] = {
            "smp_sz": smp_sz,
            "mean": mean,
            "mdn": mdn,
            "std": std,
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "spks": spks,
            "spkfreq": spkfreq,
            "sub5freq": sub5freq,
        }

        ##graphing
        # plt.plot(df["time"], df["power"])
        # plt.xlabel("Time")
        # plt.ylabel("Power (W)")
        # plt.title(f"Power Usage Over Time for the combo: {combo}")
        # plt.grid(True)
        # plt.tight_layout()
        # plt.show()


if __name__ == "__main__":
    main()

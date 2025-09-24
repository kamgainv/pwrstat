import numpy as np
import pandas as pd
import csv


def main():
    pcs = ["ollama", "sway", "plasma"]
    OGdf = pd.read_csv("./log.csv")
    dc_df = OGdf[OGdf["charging"] == 0]
    OGdf["session_list"] = OGdf["session"].fillna(" ").str.split("+").apply(sorted)
    OGdf["session_tuple"] = OGdf["session_list"].apply(tuple)
    for combo, df in OGdf.groupby("session_tuple"):
        if df.empty:
            continue
        print(combo)
        pwr = df["power"]
        mean = pwr.mean()
        mdn = pwr.median()
        std = pwr.std()
        spks = df[df["power"] >= (mdn + 2 * std)]
        print(
            f"for combo: {combo},\nmean: {mean},\nmedian:{mdn}\nstandard deviation:{std}\nAmount of spikes: \n"
        )


if __name__ == "__main__":
    main()

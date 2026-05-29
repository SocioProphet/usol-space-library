import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_altitude(df: pd.DataFrame, time_col: str, alt_col: str, title: str, path: str):
    _ = df[time_col].astype(str).values
    y = pd.to_numeric(df[alt_col], errors="coerce").values
    mask = np.isfinite(y)
    plt.figure()
    plt.plot(np.arange(mask.sum()), y[mask])
    plt.xlabel("Index (time order)")
    plt.ylabel("Altitude (deg)")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

import numpy as np


def subtract_background(signal: np.ndarray, background: np.ndarray):
    if signal.shape != background.shape:
        raise ValueError("Signal and background must have same shape")
    return signal - background

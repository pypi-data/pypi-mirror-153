""" Collection of math plots """

from typing import Optional

import numpy as np
import pandas as pd
import scipy.stats as stats
from numpy import cos, exp, pi, sin


def normal(x: np.array, mu: float = 0, sigma: float = 1) -> np.array:
    """
    :param x: xxx
    :param mu: mean
    :param sigma: standard deviation
    :returns: a normal probability distribution
    """
    return stats.norm.pdf(x, mu, sigma)


def sine_wave(t: np.array, freq: float = 1.0, amp: float = 1.0) -> np.array:
    """
    :param t: xxx
    :param freq: xxx
    :param amp: xxx
    :returns: a sine wave
    """
    return amp * sin(t * freq * 2 * pi)


def cosine_wave(t: np.array, freq: float = 1.0, amp: float = 1.0) -> np.array:
    """
    :param t: xxx
    :param freq: xxx
    :param amp: xxx
    :returns: a cosine wave
    """
    return amp * cos(t * freq * 2 * pi)


def damped_sine_wave(
    t: np.array, freq: float = 1.0, amp: float = 1.0, damp: float = 1.0
) -> np.array:
    """
    :param t: xxx
    :param freq: xxx
    :param amp: xxx
    :param damp: xxx
    :returns: a damped sine wave
    """
    return exp(-t * damp) * amp * cos(t * freq * 2 * pi)


def dataframe(**kw) -> pd.DataFrame:
    """
    :param kw: xxx
    :returns: a dataframe populated by values specified by keyword
    """
    return pd.DataFrame(kw)


def demo_df(filename: Optional[str] = None) -> pd.DataFrame:
    """Generate a dataframe and write it to filename

    :param filename: Name of the file to write generated data to.
    :returns: Generated dataframe
    """

    t = np.linspace(start=-3, stop=3, num=200)
    df = dataframe(
        time=t,
        sin=sine_wave(t, 1.0),
        cos=cosine_wave(t, 1.0),
        normal=normal(t),
        damp=damped_sine_wave(t, amp=0.5, damp=0.5),
    )

    if filename:
        df.to_csv(filename, index=False)
    return df

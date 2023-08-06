import numpy as np


def round(x: float or np.array, base: int = 5) -> float or np.array:
    """_summary_

    Parameters
    ----------
    x : float or np.array
        Number or array to be rounded
    base : int, optional
        Base to round the number, by default 5

    Returns
    -------
    float or np.array
        Rounded number
    """
    return base * np.round(x / base)

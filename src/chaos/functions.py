"""Purely mathematical functions that can be plotted and analyzed."""
from typing import Union

import numpy as np
from eliot import log_call


@log_call
def logistic(
        x: Union[float, np.ndarray],
        r: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
    """Compute the basic logistic function.

    The equation is defined as:
    :math:`x_{t+1} = r * x_t * (1 - x_t)`

    Args:
        x: The x values.
        r: The parameter to vary.

    Returns:
        np.ndarray: The computed y-values.
    """
    return r * x * (1 - x)

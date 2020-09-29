"""Main module docstring."""
from pathlib import Path
from typing import List
import argparse

from eliot import log_call, to_file
import gif
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

gif.options.matplotlib['dpi'] = 300
to_file(open('logfile.log', 'w'))


@log_call
def compute(r: float, y_start: float = 0.5, x_range: int = 100) -> List[float]:
    """Compute the y values for the logistic map shown below.

    :math:`x_{n+1} = r * x_n * (1 - x_n)`

    Args:
        r: The parameter to vary.
        y_start: The starting y value.
        x_range: The number of y values to compute.

    Returns:
        List[float]: The computed y values.

    Example:
        >>> compute(3, 0.5, 5)
        [0.5, 0.75, 0.5625, 0.73828125, 0.5796661376953125]
    """
    # This can be optimized with numpy?
    y_vals = [y_start]
    for _ in range(x_range - 1):
        y_vals.append(r * y_vals[-1] * (1 - y_vals[-1]))

    return y_vals


@gif.frame
def plot(r: float, y_start: float = 0.5, x_range: int = 100) -> None:
    """Plot function to plot the logistic map.

    Args:
        r: The parameter to vary.
        y_start: The starting y value.
        x_range: The number of y values to compute.
    """
    plt.plot(range(x_range), compute(r, y_start, x_range))


def main() -> None:
    """Create the gif.

    Generate a gif showing how the plot of a logistic map changes for
    parameter values ranging between 0 and 4.5.
    """
    frames = []
    for r in tqdm(np.linspace(start=0, stop=4.5, num=100)):
        frames.append(plot(r))

    gif.save(
        frames,
        Path() / 'src' / 'logistic_map.gif',
        duration=10,
        unit='s',
        between='startend'
    )


if __name__ == '__main__':
    main()

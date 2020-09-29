"""Main module docstring."""
import argparse
from pathlib import Path
import sys
from typing import List

from eliot import log_call, to_file
import gif
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

gif.options.matplotlib['dpi'] = 300
to_file(open('logfile.log', 'w'))


def parse_arguments():  # noqa: No type available for argparse.Namespace
    """Parse command line arguments.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            'Produce gifs visualizing chaotic behaviour. '
            'Currently only supports the simple logistic map '
            'for varying values of r.'
        )
    )
    parser.add_argument(
        '--start',
        type=float,
        default=0,
        help='The starting value for r.'
    )
    parser.add_argument(
        '--stop',
        type=float,
        default=4,
        help='The final value for r.'
    )
    parser.add_argument(
        '--n_frames',
        type=int,
        default=100,
        help='The number of frames to compute.'
    )
    parser.add_argument(
        '--gif_duration',
        type=int,
        default=10,
        help='The length of the gif in seconds.'
    )

    # When testing, call default arguments
    if sys.argv[0].find('pytest') == -1:
        args = parser.parse_args()
    else:
        args = parser.parse_args([])

    return args


@log_call
def compute_logistic_map(
        r: float,
        y_start: float = 0.5,
        x_range: int = 100) -> List[float]:
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
def plot(
        r: float,
        y_start: float = 0.5,
        x_range: int = 100) -> None:
    """Plot function to plot the logistic map.

    Args:
        r: The parameter to vary.
        y_start: The starting y value.
        x_range: The number of y values to compute.
    """
    plt.plot(range(x_range), compute_logistic_map(r, y_start, x_range))


def logistic_map_gif(
        start: float = 0,
        stop: float = 4.5,
        n_frames: int = 100,
        gif_duration: int = 10) -> None:
    """Create the gif.

    Generate a gif showing how the plot of a logistic map changes for
    parameter values ranging between 0 and 4.5.

    Args:
        start (float): Starting value for r.
        stop (float): Final value for r.
        n_frames (int): Number of frames to capture between start and stop.
        gif_duration (int): The duration of the gif to produce in seconds.
    """
    frames = []
    for r in tqdm(np.linspace(start=start, stop=stop, num=n_frames)):
        frames.append(plot(r))

    gif.save(
        frames,
        Path() / 'src' / 'logistic_map.gif',
        duration=gif_duration,
        unit='s',
        between='startend'
    )


if __name__ == '__main__':
    args = parse_arguments()
    logistic_map_gif(**vars(args))

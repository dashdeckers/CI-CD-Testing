"""Functions related to plotting and gif creation."""
from pathlib import Path
from typing import Any, Callable

from .functions import logistic

import gif
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

gif.options.matplotlib['dpi'] = 300


@gif.frame
def plot(
        x: np.ndarray,
        func: Callable,
        show: bool = False,
        **kwargs: float) -> None:
    """Plot a function.

    Args:
        x (np.ndarray): The x values.
        func (Callable): The function to plot.
        show (bool): Whether to show the plot directly.
        **kwargs (float): Possible kwargs to pass to the function.
    """
    plt.plot(x, func(x, **kwargs))
    plt.title(f'Plot of {func.__name__}')

    if show:
        plt.show()


@gif.frame
def plot_sequential(
        x0: float,
        n_values: int,
        func: Callable,
        show: bool = False,
        **kwargs: float) -> None:
    """Plot a function sequentially, taking as input the previous output.

    Args:
        x0 (float): The initial starting value.
        n_values (int): The amount of values to compute.
        func (Callable): The function to compute them with.
        show (bool): Whether to show the plot directly.
        **kwargs (float): Possible kwargs to pass to the function.
    """
    y_values = np.zeros((n_values, ))
    y_values[0] = x0

    for i in range(n_values - 1):
        y_values[i + 1] = func(y_values[i], **kwargs)

    plt.plot(range(n_values), y_values)
    plt.ylim(0, 1)
    plt.title(f'Sequential plot for {func.__name__}')

    if show:
        plt.show()


@gif.frame
def plot_bifurcation(
        x0: float,
        iwaste: int,
        iterations: int,
        r_start: float,
        r_stop: float,
        r_num: int,
        func: Callable,
        show: bool = False,
        **kwargs: float) -> None:
    """Plot the bifurcation diagram of a function.

    Args:
        x0 (float): The initial starting value.
        iwaste (int): The number of iterations to ignore.
        iterations (int): The number of iterations to plot.
        r_start (float): The starting value for r.
        r_stop (float): The end value for r.
        r_num (int): The number of r values to plot.
        func (Callable): The function to plot.
        show (bool): Whether to show the plot directly.
        **kwargs (float): Possible kwargs to pass to the function.
    """
    r = np.linspace(r_start, r_stop, r_num)
    x = x0 * np.ones(r_num)

    for i in range(iwaste + iterations):
        x = func(x, r=r)
        if i >= (iwaste):
            plt.plot(r, x, ',k', alpha=0.25)

    plt.xlim(r_start, r_stop)
    plt.title(f'Bifurcation Diagram for {func.__name__}')

    if show:
        plt.show()


def logistic_map_gif(
        x0: float = 0.5,
        n_values: int = 100,
        start: float = 0,
        stop: float = 4.5,
        n_frames: int = 100,
        gif_duration: int = 10,
        **kwargs: Any) -> None:
    """Create the sequential logistic gif.

    Generate a gif showing how the plot of a logistic map changes for
    parameter values ranging between 0 and 4.5.

    Args:
        x0 (float): The initial starting value.
        n_values (int): The amount of values to compute per frame.
        start (float): Starting value for r.
        stop (float): Final value for r.
        n_frames (int): Number of frames to capture between start and stop.
        gif_duration (int): The duration of the gif to produce in seconds.
        **kwargs (Any): Possible extra kwargs.
    """
    frames = []
    for r in tqdm(np.linspace(start=start, stop=stop, num=n_frames)):
        frames.append(plot_sequential(x0, n_values, logistic, r=r))

    gif.save(
        frames,
        Path() / 'src' / 'logistic_map.gif',
        duration=gif_duration,
        unit='s',
        between='startend'
    )

"""Test module docstring."""
from src.chaos import functions, plot


def test_plot_funcs_return_none() -> None:
    """Tests that the gif generator does not return anything."""
    assert plot.plot(1, functions.logistic, r=1) is not None
    assert plot.plot_sequential(1, 1, functions.logistic, r=1) is not None
    assert plot.plot_bifurcation(1, 1, 1, 1, 2, 1, functions.logistic) is not None

    assert plot.logistic_map_gif(0, 1, 0, 1, 2, 1) is None

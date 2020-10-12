"""Test module docstring."""
from src.chaos import functions, plot


def test_plot_funcs_return_none() -> None:
    """Tests that the gif generator does not return anything."""
    assert plot.plot(1, functions.logistic, r=1) is not None
    assert plot.plot_sequential(1, 1, functions.logistic, r=1) is not None
    assert plot.plot_bifurcation(1, 1, 1, 1, 2, 1, functions.logistic) is not None

    assert plot.logistic_map_gif(0, 1, 0, 1, 2, 1) is None


# def test_argparse_dummy() -> None:
#     """Test argparse to fool coverage minimum.

#     I trust the argparse module so I have no intention of testing
#     it rigorously.
#     """
#     args = main.parse_arguments()
#     print(args)
#     assert args.start == 0
#     assert args.stop == 4
#     assert args.n_frames == 100
#     assert args.gif_duration == 10

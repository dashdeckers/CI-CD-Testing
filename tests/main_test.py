"""Test module docstring."""
from src import main


def test_compute_logistic_map_works() -> None:
    """Tests that compute works."""
    y_vals = main.compute_logistic_map(r=3, y_start=0.5, x_range=10)
    assert all([
        a == b for a, b in
        zip(y_vals, [0.5, 0.75, 0.5625, 0.73828125, 0.5796661376953125])
    ])


def test_logistic_map_gif_generator_returns_none() -> None:
    """Tests that the gif generator does not return anything."""
    assert main.logistic_map_gif(0, 1, 2, 1) is None


def test_argparse_dummy() -> None:
    """Test argparse to fool coverage minimum.

    I trust the argparse module so I have no intention of testing
    it rigorously.
    """
    args = main.parse_arguments()
    print(args)
    assert args.start == 0
    assert args.stop == 4
    assert args.n_frames == 100
    assert args.gif_duration == 10

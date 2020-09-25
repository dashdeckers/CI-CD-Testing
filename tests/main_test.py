"""Test module docstring."""
from src import main


def test_compute_works() -> None:
    """Tests that compute works."""
    y_vals = main.compute(r=3, y_start=0.5, x_range=10)
    assert all([
        a == b for a, b in
        zip(y_vals, [0.5, 0.75, 0.5625, 0.73828125, 0.5796661376953125])
    ])

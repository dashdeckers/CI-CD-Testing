"""Main module docstring."""
import argparse
import sys

from eliot import to_file
from chaos.plot import logistic_map_gif, plot_bifurcation
from chaos.functions import logistic


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
    parser.add_argument(
        '--logging',
        type=bool,
        default=False,
        help='Whether to turn logging on or off.'
    )

    # When testing, call default arguments
    if sys.argv[0].find('pytest') == -1:
        args = parser.parse_args()
    else:
        args = parser.parse_args([])

    return args


if __name__ == '__main__':
    args = parse_arguments()
    if args.logging:
        to_file(open('logfile.log', 'w'))

    logistic_map_gif(**vars(args))
    plot_bifurcation(1e-5, 800, 200, 2.5, 4, 1000, logistic, show=True)

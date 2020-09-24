"""The environment module."""
from eliot import log_call

import numpy as np


@log_call
def do_shit(world: np.ndarray) -> np.ndarray:
    """Do some shit.

    Args:
        world (np.ndarray): Description

    Returns:
        np.ndarray: Description
    """
    return world

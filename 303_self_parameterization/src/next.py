import numpy as np

def next(he):
    """
    For a given half edge, returns the next half edge

    Inputs
        he: index of the half edge

    Outputs
        The next half edge
    """
    s = he % 3
    return (he - s) + ((s + 1) % 3)
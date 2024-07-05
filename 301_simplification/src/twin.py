def twin(twins, he):
    """
    For a given half edge index he, returns the twin half edge index

    Inputs
        twins: |hE| (== |F|*3) array of twin half-edge indices
        he: index of the half edge

    Outputs
        he_twin The twin of he
    """
    return twins[he]
def tip_vertex(tips, he):
    """
    For a given half edge, returns the tip (end point) vertex index

    Inputs
        tips: |hE| array of vertex indices
        he: he: index of the half edge

    Outputs
        v: The tip vertex index of he
    """
    return tips[he]
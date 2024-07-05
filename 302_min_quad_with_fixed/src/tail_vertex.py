from .next import next
def tail_vertex(tips, he):
    """
    For a given half edge, returns the tail (starting point) vertex index

    Inputs
        tips: |hE| array of vertex indices
        he: he: index of the half edge

    Outputs
        v: The tail vertex index of he
    """
    return tips[next(next(he))]
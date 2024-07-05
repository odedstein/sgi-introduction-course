
def face_side_to_half_edge_index(fs):
    """
    given face side (fs) compute the half edge index
    """
    return (fs[0]*3) + fs[1]

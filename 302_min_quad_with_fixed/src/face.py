def face(he):
    """
    get the face index of an half edge

    Input
        he: (1,) half edge index

    Output
        f: (1,) face index of the half edge
    """
    return he // 3
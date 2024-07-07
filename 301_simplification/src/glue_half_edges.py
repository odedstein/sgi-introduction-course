def glue_half_edges(twin_he_all, he0, he1):
    twin_he_all[he0] = he1
    twin_he_all[he1] = he0
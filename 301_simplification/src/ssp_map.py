class ssp_map:
    def __init__(self, ij_indices, UV, F_pre, F_post, fIdx_pre, fIdx_post):
        self.i = ij_indices[0]
        self.j = ij_indices[1]
        self.UV = UV
        self.F_pre = F_pre
        self.F_post = F_post
        self.fIdx_pre = fIdx_pre
        self.fIdx_post = fIdx_post

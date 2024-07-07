import numpy as np 
from .normalize_row import normalize_row

def face_normals(V, F, f = None):    
	'''
	computes unit face normal of a triangle mesh

	Inputs:
        V: |V|x3 numpy ndarray of vertex positions
        F: |F|x3 numpy ndarray of face indices
		f: (optional) a subset of face indices 
	
	Outputs:
	    FN: |F|x3 (or |f|x3) numpy ndarray of unit face normal 
	'''
	if np.isscalar(f): # f is a integer
		vec1 = V[F[f,1],:] - V[F[f,0],:]
		vec2 = V[F[f,2],:] - V[F[f,0],:]
		FN = np.cross(vec1, vec2)
		return FN / np.linalg.norm(FN)
	if f is None: # compute all
		vec1 = V[F[:,1],:] - V[F[:,0],:]
		vec2 = V[F[:,2],:] - V[F[:,0],:]
	else: # compute a subset
		vec1 = V[F[f,1],:] - V[F[f,0],:]
		vec2 = V[F[f,2],:] - V[F[f,0],:]
	FN = np.cross(vec1, vec2) 
	return normalize_row(FN)
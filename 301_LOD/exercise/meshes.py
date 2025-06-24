from curves import *

def area_weighted_face_normal(v0: np.ndarray, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
	'''
	Args: 
		The 3D positions of the three vertex positions defining an oriented triangle, 
		given as length-3 NumPy arrays.

	Returns:
		The normal vector of the triangle, multiplied by the face's area.
	'''
	return np.array([1., 0.]) # TODO

def all_vertex_quadrics(vertices: np.ndarray, faces: np.ndarray) -> list[np.ndarray]:
	'''
	Compute quadric error matrix for each vertex

	Args:
		vertices: |V| x 3 NumPy array
		faces: |F| x 3 integer-valued NumPy array

	Returns:
		length-|V| list of NumPy matrices of shape 4 x 4 
	'''
	quadrics = [np.zeros((4, 4)) for _ in range(len(vertices))]
	# TODO
	return quadrics

def cost(v: np.ndarray, Q: np.ndarray) -> float:
	'''
	Compute the quadric error of a vertex position

	Args:
		v: NumPy array of size (3,) representing a position in R^3, expressed in homogeneous coordinates.
		Q: 4 x 4 NumPy matrix representing a quadric error matrix.

	Returns:
		Cost of v relative to Q (sum of squared distances to the union of planes represented by Q).

	Warning: Matrix multiplication between NumPy matrices/vectors is done via the `@` symbol!
	'''
	return 0. # TODO

def edge_collapse_cost(edge: tuple[int,int], vertices: np.ndarray, quadrics: list[np.ndarray]) -> float:
	'''
	Compute the cost and optimal position of collapsing an edge.

	Args:
		edge: 2-tuple (v0, v1) of vertex indices defining an edge
		vertices: |V| x 3 NumPy array
		quadrics: length-|V| list of NumPy matrices of shape 4 x 4

	Returns:
		A 2-tuple (cost, v^*) containing the cost of collapse, and the location of the optimal point of collapse v^*. 
	'''

	v0, v1 = edge
	return 0., vertices[v0,:] # TODO

def is_face_valid(faces: np.ndarray, keep_vertex: np.ndarray) -> bool:
	'''
	Return True if face(s) remains valid.

	Args:
		faces: _ x 3 integer-valued NumPy array
		keep_vertex: length-|V| array, where i-th element is True if the i-th vertex is valid
	'''
	# Check that all vertices are valid.
	all_valid = np.all(keep_vertex[faces], axis=1)

	# Check for duplicate vertices.
	sorted_faces = np.sort(faces, axis=1)
	no_duplicates = np.all(np.diff(sorted_faces, axis=1) > 0, axis=1)

	return all_valid & no_duplicates

def edges_adjacent_to_vertex(v_idx: int, adjacent_faces: np.ndarray):
	'''
	Find all edges connected to a given vertex

	Args:
		v_idx: index of vertex
		adjacent_faces: _ x 3 array of faces containing the vertex

	Returns:
		list of 2-tuples, each reprsenting an edge
	'''
	
	# Create all edges from adjacent faces
	edges_array = np.array([
		[adjacent_faces[:, 0], adjacent_faces[:, 1]],
		[adjacent_faces[:, 1], adjacent_faces[:, 2]],
		[adjacent_faces[:, 2], adjacent_faces[:, 0]]
	]).transpose(0, 2, 1).reshape(-1, 2)  # Shape: (3*|adjacent_faces|, 2)
	
	# Filter edges that contain the vertex
	vertex_mask = np.any(edges_array == v_idx, axis=1)
	vertex_edges = edges_array[vertex_mask]
	
	# Find unique edges (by sorting each edge so smaller vertex index comes first)
	unique_edges = np.unique(np.sort(vertex_edges, axis=1), axis=0)
	
	return [tuple(edge) for edge in unique_edges]

def all_edges(faces: np.ndarray) -> np.ndarray:
	'''
	Find all unique edges in the mesh.

	Args:
		faces: |F| x 3 integer-valued NumPy array

	Returns:
		list of 2-tuples, each representing an edge
	'''

	# Create all edges from adjacent faces
	edges_array = np.array([
		[faces[:, 0], faces[:, 1]],
		[faces[:, 1], faces[:, 2]],
		[faces[:, 2], faces[:, 0]]
	]).transpose(0, 2, 1).reshape(-1, 2)  # Shape: (3*|faces|, 2)

	# Find unique edges (by sorting each edge so smaller vertex index comes first)
	unique_edges = np.unique(np.sort(edges_array, axis=1), axis=0)

	return [tuple(edge) for edge in unique_edges]

def quadric_error_simplify_mesh(vertices: np.ndarray, faces: np.ndarray, target_vertices: int):
	'''
	Args:
		vertices: |V| x 3 NumPy array
		faces: |F| x 3 integer-valued NumPy array

	Returns:
		A |V|' x 3 NumPy array encoding the vertices of the simplified triangle mesh.
		A |F|' x 3 integer-valued NumPy array encoding the faces of the simplified triangle mesh.
	'''
	
	"""
	Notes: 

	- If you want to use a PriorityQueue, the syntax for creating a queue and adding items is as follows: 

		q = PriorityQueue()
		q.put((2.5, item_0))

	If you want to pop an item from the top of the queue, use `q.get()`. 
	This both returns the item, and pops it from the queue. By default, the item with the *lowest* priority value is 
	popped first.
	
	You can check if a queue is empty by checking the value of `q.empty()`, which returns True if `q` has zero items.

	Also feel free to use any of the pre-implemented helper functions above (is_face_valid, edges_adjacent_to_vertex, all_edges)
	or not. Completely up to you!
	"""

	return vertices, faces
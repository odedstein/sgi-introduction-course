from curves import *

def area_weighted_face_normal(v0: np.ndarray, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
	'''
	Args: 
		The 3D positions of the three vertex positions defining an oriented triangle, 
		given as length-3 NumPy arrays.

	Returns:
		The normal vector of the triangle, multiplied by the face's area.
	'''
	n = np.cross(v1 - v0, v2 - v0)
	return 0.5*n

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
	
	for face in faces:
		v0, v1, v2 = vertices[face]

		area_normal = area_weighted_face_normal(v0, v1, v2)
		face_area = np.linalg.norm(area_normal)
		normal = area_normal / face_area
		plane = np.array([normal[0], normal[1], normal[2], -np.dot(normal, v0)])
		quadric = np.outer(plane, plane)
		
		# Add the area-weighted quadric to all three vertices of the face.
		for v_idx in face:
			quadrics[v_idx] += face_area*quadric
	
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
	w = np.array([v[0], v[1], v[2], 1.])
	return w.T @ Q @ w

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
	
	Q = quadrics[v0] + quadrics[v1]
	A = Q[:3, :3]
	b = -Q[:3, 3]
	
	p = np.linalg.lstsq(A, b)[0]
	return cost(p, Q), p

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
	"""
	
	n_vertices = vertices.shape[0]
	n_faces = faces.shape[0]
	if n_vertices <= target_vertices or target_vertices <= 4:
		return vertices, faces
	
	# Compute quadric error matrix for each vertex.
	quadrics = all_vertex_quadrics(vertices, faces)
	
	# Find all unique edges and compute collapse costs; add them to the queue.
	edges = all_edges(faces)
	q = PriorityQueue()
	for edge in edges:
		cost, new_pos = edge_collapse_cost(edge, vertices, quadrics)
		q.put((cost, (edge, new_pos)))
	
	new_positions = copy.deepcopy(vertices)
	current_faces = copy.deepcopy(faces)
	vertex_map = np.arange(n_vertices) # i-th entry gives the index of the vertex that the i-th vertex got merged into
	keep_vertex = np.full(n_vertices, True)
	keep_face = np.full(n_faces, True)
	n_vertices_kept = n_vertices
	while not q.empty():
		cost, item = q.get()
		edge, new_pos = item
		v0, v1 = edge

		# Check if this edge is still valid:
		# Skip if either vertex has already been deleted (merged with another).
		if not keep_vertex[v0] or not keep_vertex[v1]:
			continue

		# Vertices may have merged with other vertices since this edge was added to the queue.
		v0 = vertex_map[v0]
		v1 = vertex_map[v1]

		# Collapse edge. Arbitrarily decide to always keep the first vertex in the tuple, and update its position.
		# For each edge involving the newly-positioned vertex, update its optimal point of collapse and cost.
		keep_vertex[v1] = False
		vertex_map[v1] = v0
		new_positions[v0] = new_pos
		quadrics[v0] = quadrics[v0] + quadrics[v1]

		# For all affected faces, check if it remains valid.
		current_faces[current_faces == v1] = v0
		updated_faces = np.where(np.any(current_faces == v0, axis=1))[0] # indices of faces whose vertices were updated
		keep_face[updated_faces] = is_face_valid(current_faces[updated_faces], keep_vertex)

		# Rather than updating the vertex indices of edges already in the queue, simply add edges containing this new vertex. 
		# Any defunct edges will be ignored by the two if-continue statements at the beginning of the while-loop.
		new_edges = edges_adjacent_to_vertex(v0, faces[updated_faces])
		for new_edge in new_edges:
			ev0, ev1 = new_edge
			if not keep_vertex[ev0] or not keep_vertex[ev1]:
				continue
			cost, new_pos = edge_collapse_cost(new_edge, new_positions, quadrics)
			q.put((cost, (new_edge, new_pos)))

		n_vertices_kept -= 1
		if n_vertices_kept <= target_vertices:
			break
			
	
	# Create vertex/face arrays of the new mesh.
	new_vertex_map = np.full(n_vertices, -1, dtype=np.int64) # i-th entry gives the index of vertex i in the new mesh
	keep_indices = np.where(keep_vertex)[0]
	new_vertex_map[keep_indices] = np.arange(len(keep_indices))

	new_vertices = new_positions[keep_vertex]
	new_faces = new_vertex_map[current_faces[keep_face]]

	return new_vertices, new_faces
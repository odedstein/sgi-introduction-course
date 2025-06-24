import numpy as np
import scipy as sp
import copy
import typing
from queue import PriorityQueue
import matplotlib.pyplot as plt

def size(curves: list[list[np.ndarray]]) -> int:
	'''
	Return the number of vertices in a collection of curves.
	'''
	n_points = sum([len(curve) for curve in curves])
	return n_points

# =================================== RDP =================================== #

def point_to_line_segment_distance(point: np.ndarray, tail: np.ndarray, tip: np.ndarray) -> float:
	'''
	Args:
		point: position in the 2D plane R^2,represented as NumPy array of size (2,)
		tail: one of the endpoints of a line segment; a position in the 2D plane R^2, 
			  represented as NumPy arrays of size (2,)
		tip: the other endpoint of a line segment; a position in the 2D plane R^2, 
			 represented as NumPy arrays of size (2,)

	Returns:
		The Euclidean distance of `point` to the line segment defined by the endpoint positions `tail` and `tip`.
	'''
	u = point - tail
	seg = tip - tail
	length2 = np.dot(seg, seg)
	if length2 == 0: 
		return np.sqrt(np.dot(u,u))

	# Vector from `point` to the closest point on the segment.
	d = u - seg * np.clip(np.dot(u, seg) / length2, 0.0, 1.0);
	return np.sqrt(np.dot(d,d))

def rdp_simplify_curve(curve: list[np.ndarray], epsilon: float) -> list[np.ndarray]:
	'''
	Recursive helper to function `rdp_simplify_curves`, which simplifies a single curve component.

	Args: 
		 curve: a list of 2D point positions, represented as NumPy arrays of size (2,)
		 epsilon: parameter controlling how coarse the final curve is

	Returns:
		 new_curve: a list of 2D point positions for the simplified curve
	'''

	# if len(curve) == 2: return curve

	# Find the point p^* in the curve farthest away from the line segment connecting the endpoints.
	p_star = 0 # index of p^*
	max_distance = 0
	for i in range(1, len(curve)-1):
		dist = point_to_line_segment_distance(curve[i], curve[0], curve[-1])
		if dist > max_distance:
			max_distance = dist
			p_star = i

	# If p^* is farther than ε to the line segment, recurse.
	# Otherwise, delete any points that are not marked "to keep", and terminate.
	new_curve = []
	if max_distance > epsilon:
		# Recurse on the two polylines with endpoints (curve[0], p^*) and (p^*, curve[-1]).
		# Keep in mind Python passes mutable data structures, like lists, by reference, but that shouldn't matter here...
		curve0 = rdp_simplify_curve(curve[0:p_star+1], epsilon)
		curve1 = rdp_simplify_curve(curve[p_star:], epsilon)
		# Avoid duplicating the point p^*, which is shared amongst the two sub-segments.
		new_curve = curve0[:-1] + curve1[:]
	else:
		new_curve = [curve[0], curve[-1]]

	# Terminate when no more simplification can be done.
	return new_curve

def rdp_simplify_curves(curves: list[list[np.ndarray]], epsilon: float=0.02) -> list[list[np.ndarray]]:
	'''
	Applies the Ramer-Douglas-Peucker algorithm for simplifying curves.
	Internally, calls the recursive function `rdp_helper`.

	Args:
		curves: list of lists, where each sublist is a sequence of 2D positions representing a connected curve component

	Returns:
		new_curves: list of lists, where each sublist is a sequence of 2D positions representing a connected curve component
	'''

	new_curves = []
	for curve in curves:
		new_curve = rdp_simplify_curve(curve, epsilon)
		new_curves.append(new_curve)

	return new_curves

# =================================== QES =================================== #

def all_quadrics(curves: list[list[np.ndarray]]) -> list[np.ndarray]:
	'''
	Compute quadric error matrix for each vertex in the curve.

	Args:
		curves: List of lists, where each sublist is a sequence of 2D positions representing a connected curve component; 2D point positions are represented as NumPy arrays of size (2,), and edge is defined between each pair of consecutive vertices in each sublist.

	Returns:
		Nested list `quadrics` of the same dimensions of `curves`, such that `quadrics[i][j]` gives the 3x3 quadric error matrix for the curve vertex at `curves[i][j]`.
	'''
	# Compute the quadric error matrix Q_i for each vertex i (minus the endpoints).
	quadrics = [[np.zeros((3, 3)) for j in range(len(curves[i]))] for i in range(len(curves))]
	for i in range(len(curves)):
		# interior points
		for j in range(1, len(curves[i])-1):
			# Construct unit normals to each adjacent edge.
			t_a = curves[i][j] - curves[i][j-1]
			t_b = curves[i][j+1] - curves[i][j]
			len_a = np.linalg.norm(t_a)
			len_b = np.linalg.norm(t_b)
			# Construct the normals by rotating tangent vectors 90 degrees. 
			# Because we are measuring *squared* distance, the direction of the normals doesn't actually matter.
			n_a = np.array([-t_a[1], t_a[0]]) 
			n_b = np.array([-t_b[1], t_b[0]])
			n_a /= np.linalg.norm(n_a)
			n_b /= np.linalg.norm(n_b)
			# Construct a 3 x 1 vector representing the tangent plane of each edge.
			p_a = np.array([n_a[0], n_a[1], -np.dot(n_a, curves[i][j])]) # plane offsets can be constructed with any point on the plane
			p_b = np.array([n_b[0], n_b[1], -np.dot(n_b, curves[i][j])])
			# Add them to the quadric! Weight by edge lengths.
			quadrics[i][j] += len_a * np.outer(p_a, p_a)
			quadrics[i][j] += len_b * np.outer(p_b, p_b)

	return quadrics

def collapse_cost(v: np.ndarray, Q: np.ndarray) -> float:
	'''
	Compute the quadric error of a vertex position.

	Args:
		v: NumPy array of size (2,) representing a position in R^2, expressed in homogeneous coordinates.
		Q: 3 x 3 NumPy matrix representing a quadric error matrix.

	Returns:
		Cost of v relative to Q (sum of squared distances to the union of planes represented by Q).

	Warning: Matrix multiplication between NumPy matrices/vectors is done via the `@` symbol!
	'''
	v_h = np.array([v[0], v[1], 1.0])
	cost = v_h.T @ Q @ v_h
	return cost

def optimal_collapse_location(Q1: np.ndarray, Q2: np.ndarray, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
	'''
	Args:
		Q1, Q2: 3 x 3 NumPy matrices representing the quadric error matrices of two endpoints of an edge.
		v1, v2: 3D positions of the two endpoints of the edge

	Returns:
		The 3D position of the optimal location of edge collapse as a (3,) NumPy vector. 

	Warning: Matrix multiplication between NumPy matrices is done via the `@` symbol!
	'''
	Q = Q1 + Q2

	# Try to solve the linear system for the optimal position
	# We want to minimize v^T * Q * v where v = [x, y, 1]^T
	# Taking derivative and setting to 0: Q * v = 0
	# Since the last component is 1, we solve for [x, y]

	A = Q[:2, :2]  # 2 x 2 upper-left block
	b = -Q[:2, 2]  # negative of the third column (first two elements)

	if np.linalg.det(A) > 1e-10: # Check if matrix is invertible
		optimal_pos = np.linalg.solve(A, b)
		return optimal_pos

	# If system is not solvable, return the midpoint of the two vertices.
	return 0.5 * (v1 + v2)

def quadric_error_simplify_curves(curves: list[list[np.ndarray]], target_vertices: int) -> list[list[np.ndarray]]:
	'''
	Applies a 1D version of the quadric error simplification algorithm for simplifying curves.

	Args:
		curves: list of lists, where each sublist is a sequence of 2D positions representing a connected curve component; 2D point positions are represented as NumPy arrays of size (2,), and edge is defined between each pair of consecutive vertices in each sublist. target_vertices: integer giving a lower bound for the number of vertices

	Returns:
		new_curves: list of lists, where each sublist is a sequence of 2D positions representing a connected curve 
					component. The total number of vertices in the curves should be as close as possible to 
				   `target_vertices`, but not below.
	'''

	n_vertices = size(curves)
	if n_vertices <= target_vertices: return curves

	# Compute the quadric error matrix Q_i for each vertex i (minus the endpoints).
	quadrics = all_quadrics(curves)

	# For each edge, compute the optimal contraction target vertex `v` (involves solving a linear system). 
	# The cost of collapsing this edge is v^T(Q_1 + Q_2)v, where Q_1, Q_2 are the quadric error matrices associated with the edge's two endpoints.
	# Record each edge (via its two vertices), the optimal vertex, and the associated cost of collapse in a priority queue.
	q = PriorityQueue()
	for i in range(len(curves)):
		for j in range(1, len(curves[i])-2): # don't consider collapses involving endpoints
			Q1 = quadrics[i][j]
			Q2 = quadrics[i][j+1]
			v_star = optimal_collapse_location(Q1, Q2, curves[i][j], curves[i][j+1])
			v_star_h = np.array([v_star[0], v_star[1], 1.0]) # homogeneous coordinates
			cost = v_star_h.T @ (Q1 + Q2) @ v_star_h
			q.put((cost, ((i,j), (i,j+1), v_star)))
	
	keep = [[True for j in range(len(curves[i]))] for i in range(len(curves))]
	new_positions = [[curves[i][j] for j in range(len(curves[i]))] for i in range(len(curves))]
	n_vertices_kept = n_vertices
	while not q.empty():
		# Pop edge with the least cost.
		cost, item = q.get()
		v_a, v_b, v_star = item

		# Skip if either vertex has already been deleted
		if not keep[v_a[0]][v_a[1]] or not keep[v_b[0]][v_b[1]]:
			continue

		# Collapse edge by deleting v_b, and setting v_a to the new position.
		keep[v_b[0]][v_b[1]] = False
		new_positions[v_a[0]][v_a[1]] = v_star

		# Update the costs of all pairs involving the deleted vertex.
		quadrics[v_a[0]][v_a[1]] = quadrics[v_a[0]][v_a[1]] + quadrics[v_b[0]][v_b[1]] # quadric of the new vertex
		
		curve_idx = v_a[0]
		vertex_idx = v_a[1]

		# Check and update edge to the left (if it exists and is valid)
		if vertex_idx > 1 and keep[curve_idx][vertex_idx-1]:
			left_vertex = (curve_idx, vertex_idx-1)
			Q1 = quadrics[left_vertex[0]][left_vertex[1]]
			Q2 = quadrics[v_a[0]][v_a[1]]
			v_star_new = optimal_collapse_location(Q1, Q2, new_positions[left_vertex[0]][left_vertex[1]], new_positions[v_a[0]][v_a[1]])
			v_star_h = np.array([v_star_new[0], v_star_new[1], 1.0])
			cost_new = collapse_cost(v_star_new, Q1 + Q2)
			q.put((cost_new, (left_vertex, v_a, v_star_new)))
			
		# Check and update edge to the right (if it exists and is valid)
		if vertex_idx < len(curves[curve_idx])-2 and keep[curve_idx][vertex_idx+1]:
			right_vertex = (curve_idx, vertex_idx+1)
			Q1 = quadrics[v_a[0]][v_a[1]]
			Q2 = quadrics[right_vertex[0]][right_vertex[1]]
			v_star_new = optimal_collapse_location(Q1, Q2, new_positions[v_a[0]][v_a[1]], new_positions[right_vertex[0]][right_vertex[1]])
			v_star_h = np.array([v_star_new[0], v_star_new[1], 1.0])
			cost_new = collapse_cost(v_star_new, Q1 + Q2)
			q.put((cost_new, (v_a, right_vertex, v_star_new)))

		# Count the number of vertices we've decided to keep so far
		n_vertices_kept -= 1
		if n_vertices_kept <= target_vertices:
			break
	
	new_curves = []
	for i in range(len(curves)):
		new_curve = []
		for j in range(len(curves[i])):
			if keep[i][j]:
				new_curve.append(new_positions[i][j])
		if len(new_curve) > 0:
			new_curves.append(new_curve)

	return new_curves

# =================================== EVALUATION =================================== #

def average_squared_error(curves1: list[list[np.ndarray]], curves2: list[list[np.ndarray]]) -> float:
	'''
	Args:
		curves1, curves2: two sets of curves

	Returns:
		The average squared error between the two curves, as defined in the README.
	'''
	n_vertices1 = size(curves1)
	n_vertices2 = size(curves2)
	d2_1 = 0.
	d2_2 = 0.
	# For each vertex in curves1...
	for curve1 in curves1:
		for v in curve1:
			min_dist = np.inf
			# ... iterate over all segments in curve2
			for curve2 in curves2:
				n_nodes = len(curve2)
				for i in range(n_nodes-1):
					tail = curve2[i]
					tip = curve2[i+1]
					min_dist = min(min_dist, point_to_line_segment_distance(v, tail, tip))
		d2_1 += min_dist*min_dist

	# For each vertex in curves2...
	for curve2 in curves2:
		for v in curve2:
			min_dist = np.inf
			# ... iterate over all segments in curve1
			for curve1 in curves1:
				n_nodes = len(curve1)
				for i in range(n_nodes-1):
					tail = curve1[i]
					tip = curve1[i+1]
					min_dist = min(min_dist, point_to_line_segment_distance(v, tail, tip))
		d2_2 += min_dist*min_dist

	return (d2_1 + d2_2)  / (n_vertices1 + n_vertices2)

def hausdorff_distance(curves1: list[list[np.ndarray]], curves2: list[list[np.ndarray]]) -> float:
	'''
	Args:
		curves1, curves2: two sets of curves

	Returns:
		The Hausdorff distance between the two curves.
	'''
	n_vertices1 = size(curves1)
	n_vertices2 = size(curves2)
	d1 = 0.
	d2 = 0.
	# For each vertex in curves1...
	for curve1 in curves1:
		for v in curve1:
			dist = 0.
			# ... iterate over all segments in curve2
			for curve2 in curves2:
				n_nodes = len(curve2)
				for i in range(n_nodes-1):
					tail = curve2[i]
					tip = curve2[i+1]
					dist = max(dist, point_to_line_segment_distance(v, tail, tip))
		d1 += dist

	# For each vertex in curves2...
	for curve2 in curves2:
		for v in curve2:
			dist = 0.
			# ... iterate over all segments in curve1
			for curve1 in curves1:
				n_nodes = len(curve1)
				for i in range(n_nodes-1):
					tail = curve1[i]
					tip = curve1[i+1]
					dist = max(dist, point_to_line_segment_distance(v, tail, tip))
		d2 += dist

	return max(d1, d2)


def frechet_distance_helper(ca, i, j, P: list[list[np.ndarray]], Q: list[list[np.ndarray]]) -> float:
	if ca[i, j] > -1:
		return ca[i, j]
	elif i == 0 and j == 0:
		ca[i, j] = np.linalg.norm(P[i]-Q[j])
	elif i > 0 and j == 0:
		ca[i, j] = max(frechet_distance_helper(ca, i-1, 0, P, Q), np.linalg.norm(P[i]-Q[j]))
	elif i == 0 and j > 0:
		ca[i, j] = max(frechet_distance_helper(ca, 0, j-1, P, Q), np.linalg.norm(P[i]-Q[j]))
	elif i > 0 and j > 0:
		ca[i, j] = max(
			min(
				frechet_distance_helper(ca, i-1, j, P, Q),
				frechet_distance_helper(ca, i-1, j-1, P, Q),
				frechet_distance_helper(ca, i, j-1, P, Q)
			),
			np.linalg.norm(P[i]-Q[j])
			)
	else:
		ca[i, j] = float('inf')

	return ca[i, j]

def discrete_frechet_distance(curves1: list[list[np.ndarray]], curves2: list[list[np.ndarray]]) -> float:
	'''
	Args:
		curves1, curves2: two sets of curves

	Returns:
		The Fréchet distance between the two curves.
	'''
	p = size(curves1)
	q = size(curves2)
	ca = (np.ones((p, q), dtype=np.float64) * -1)
	P = [p for curve in curves1 for p in curve]
	Q = [p for curve in curves2 for p in curve]
	dist = frechet_distance_helper(ca, p-1, q-1, P, Q)
	return dist

def plot_errors(curves: list[list[np.ndarray]]) -> None:
	'''
	Graph error vs. number of vertices of each curve simplification method, applied to the given set of curves.

	Args:
		curves: Input curves to be simplified.

	Returns:
		None
	'''

	n_samples = 12
	# Arbitrarily choose some vertex numbers at which to sample QES.
	n_vertices = size(curves)
	V = [n_vertices // (2*i) for i in range(1,n_samples+1)] # least to most simplified
	# Arbitrarily choose some epsilons at which to sample RDP.
	epsilons = [10**(-i) for i in range(1,n_samples+1)] # most to least simplified

	# Run each method!
	QES_errors = [0 for i in range(n_samples)]
	QES_vertices = [0 for i in range(n_samples)]
	RDP_errors = [0 for i in range(n_samples)]
	RDP_vertices = [0 for i in range(n_samples)]
	QES_curves = copy.deepcopy(curves)
	RDP_curves = copy.deepcopy(curves)
	for i in range(n_samples):
		# QES
		target_vertices = V[i]
		QES_curves = quadric_error_simplify_curves(QES_curves, target_vertices)
		QES_errors[i] = discrete_frechet_distance(curves, QES_curves)
		QES_vertices[i] = size(QES_curves)
		# RDP
		idx = n_samples-i-1
		eps = epsilons[idx]
		RDP_curves = rdp_simplify_curves(RDP_curves, eps)
		RDP_errors[idx] = discrete_frechet_distance(curves, RDP_curves)
		RDP_vertices[idx] = size(RDP_curves)

	plt.loglog(RDP_vertices, RDP_errors, linewidth=2, label='RDP')
	plt.loglog(QES_vertices, QES_errors, linewidth=2, label='QES')
	plt.legend()
	plt.xlabel('Number of vertices')
	plt.ylabel('Error')
	plt.title('Error vs. number of vertices')
	plt.show()

# =================================== ADAPTIVE INTEGRATION =================================== #

def electric_field(V: np.ndarray) -> np.ndarray:
	'''
	Evaluate a particular electric field defined in 2D.

	Args:
		An array of positions at which to evaluate an electric field.

	Returns:
		The electric field vector at the given position(s). 

	'''
	X = V[:,0]
	Y = V[:,1]
	E = np.transpose(np.vstack((np.exp(-(X*X + Y*Y)), np.sin(X))))
	return E

def adaptively_sample_curve(interval: tuple[float, float], epsilon: float) -> np.ndarray:
	'''
	Recursive function similar to `rdp_simplify_curve`, which samples a single curve component.

	Args: 
		interval: Endpoints of an interval of the smooth curve γ(t) = (2πt - π, sin(2πt)), specified as parameter values.
		epsilon: Error threshold.

	Returns:
		samples: A list of parameter values at which to sample the curve.
	'''

	# Roughly speaking, we want to sample more where |g''(t)| is large.
	# Here, we just re-purpose the RDP algorithm above.
	# If (length)^3/12 * g^* > ε, recurse.
	t0 = interval[0]
	t1 = interval[1]
	h = t1-t0

	def g_abs_curvature(t):
		'''
		Compute |g''(t)|.
		'''
		k = np.pi*(-2.*(1.+4.*np.pi*np.pi)*np.cos(2.*np.pi*t)*np.sin(t) + 8.*np.exp(-t*t-np.sin(t)*np.sin(t)) * (t + np.cos(t)*(-1.+np.sin(t)))*(t+np.cos(t)*(1.+np.sin(t))) - 8.*np.pi*np.cos(t)*np.sin(2.*np.pi*t))
		return np.abs(k)

	def g(t):
		'''
		Compute g(t).
		'''
		g = np.array([t, 2.*np.pi*(np.exp(-t*t-np.sin(t)*np.sin(t)) + np.sin(t)*np.cos(2.*np.pi*t))])
		g = g.flatten()
		return g

	def g_distance_to_segment(t):
		'''
		Compute the (negative) distance of g(t) to the line segment connecting g(t0) and g(t1). 
		'''
		return -point_to_line_segment_distance(g(t), g(t0), g(t1))

	# Find the point p^* in the curve farthest away from the line segment connecting the endpoints.
	res = sp.optimize.minimize(g_distance_to_segment, np.array([t0]), bounds=(interval,))
	t_star = res.x[0]
	k = g_abs_curvature(t_star)
	error = h*h*h/12 * k

	# If p^* is farther than ε to the line segment, recurse.
	# Otherwise, delete any points that are not marked "to keep", and terminate.
	new_curve = []
	if error > epsilon:
		# Recurse on the two polylines with endpoints (curve[0], p^*) and (p^*, curve[-1]).
		# Keep in mind Python passes mutable data structures, like lists, by reference, but that shouldn't matter here...
		curve0 = adaptively_sample_curve((t0, t_star), epsilon)
		curve1 = adaptively_sample_curve((t_star, t1), epsilon)
		# Avoid duplicating the point p^*, which is shared amongst the two sub-segments.
		new_curve = curve0[:-1] + curve1[:]
	else:
		new_curve = [t0, t1]

	# Terminate when no more simplification can be done.
	return new_curve



def adaptive_integration(epsilon: float=0.01) -> tuple[list[np.ndarray], list[np.ndarray]]:
	'''
	Adaptively integrate the electric field E(x,y) = (e^{-r^2}, sin(x)) along the curve γ(t) = (2πt - π, sin(2πt)).
	There are many ways you might approach this problem... this is just one approach that maybe kind of sensible 
	(but by no means the best!) In fact, it's not strictly guaranteed to get under the given error threshold -- and
	if you were to run this code, perhaps you can see how it might do better :)

	Args:
		epsilon: Target error threshold below; we aim to get the integration error below this threshold.

	Returns:
		Two curves: A finely sampled version of the smooth curve γ, and a sampled version of the curve.
	'''

	# Finely sample the curve, for visualization.
	n_smooth_samples = 256
	t = np.linspace(0., 1., n_smooth_samples)
	smooth_curve = np.transpose(np.vstack((2.*np.pi*t - np.pi, np.sin(2.*np.pi*t))))
	smooth_estimate = 0.
	for i in range(n_smooth_samples-1):
		gamma_0 = np.reshape(smooth_curve[i,:], (1,-1))
		gamma_1 = np.reshape(smooth_curve[i+1,:], (1,-1))
		gamma_vector = gamma_1 - gamma_0
		smooth_estimate += np.dot(gamma_vector.flatten(),  0.5*(electric_field(gamma_0) + electric_field(gamma_1)).flatten())

	# TODO: sample curve!
	samples = adaptively_sample_curve((0., 1.), epsilon)
	samples = np.array(samples)
	sampled_curve = np.transpose(np.vstack((2.*np.pi*samples - np.pi, np.sin(2.*np.pi*samples)))) # get positions

	estimate = 0.
	n_samples = len(sampled_curve)
	for i in range(n_samples-1):
		gamma_0 = np.reshape(sampled_curve[i,:], (1,-1))
		gamma_1 = np.reshape(sampled_curve[i+1,:], (1,-1))
		gamma_vector = gamma_1 - gamma_0
		estimate += np.dot(gamma_vector.flatten(),  0.5*(electric_field(gamma_0) + electric_field(gamma_1)).flatten())

	print(f"True integral value (approximate): {smooth_estimate}")
	print(f"Numerical approximation: {estimate}")
	print(f"Integration error (relative): {(estimate-smooth_estimate)/smooth_estimate}")
	print("Number of samples used to compute true value vs. approximate: %d\t%d" %(n_smooth_samples, n_samples))
	return smooth_curve, sampled_curve


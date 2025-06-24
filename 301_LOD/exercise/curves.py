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
	return 0. # TODO

def rdp_simplify_curve(curve: list[np.ndarray], epsilon: float) -> list[np.ndarray]:
	'''
	Recursive helper to function `rdp_simplify_curves`, which simplifies a single curve component.

	Args: 
		 curve: a list of 2D point positions, represented as NumPy arrays of size (2,)
		 epsilon: parameter controlling how coarse the final curve is

	Returns:
		 new_curve: a list of 2D point positions for the simplified curve
	'''

	return curve # TODO

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
		# iterate over interior points
		for j in range(1, len(curves[i])-1):
			pass # TODO

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
	return 0. # TODO

def optimal_collapse_location(Q1: np.ndarray, Q2: np.ndarray, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
	'''
	Args:
		Q1, Q2: 3 x 3 NumPy matrices representing the quadric error matrices of two endpoints of an edge.
		v1, v2: 3D positions of the two endpoints of the edge

	Returns:
		The 3D position of the optimal location of edge collapse as a (3,) NumPy vector. 

	Warning: Matrix multiplication between NumPy matrices is done via the `@` symbol!
	'''
	return np.array([0., 0.]) # TODO

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


def discrete_frechet_distance(curves1: list[list[np.ndarray]], curves2: list[list[np.ndarray]]) -> float:
	'''
	Args:
		curves1, curves2: two sets of curves

	Returns:
		The Fréchet distance between the two curves.
	'''
	return 0.

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
	sampled_curve = smooth_curve

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


import os
import argparse
import time

import polyscope as ps
import polyscope.imgui as psim

from meshes import *

def read_curve(filepath):
	'''
	Read a polyline from a custom file format.

	Args:
		filepath: string

	Returns:
		curves: list of lists, where each sublist is a sequence of 2D positions representing a connected curve component
	'''
	curves = []
	vertices = []
	with open(filepath, "r") as file:
		for line in file:
			parts = line.strip().split()
			if not parts:
				continue
			elif parts[0] == "v":
				pos = list(map(float, parts[1:3]))
				vertices.append(pos)
			elif parts[0] == "l":
				idxs = list(map(int, parts[1:]))
				curve = [np.array(vertices[idx-1], dtype=np.float64) for idx in idxs]
				curves.append(curve)

	return curves

def visualize_curve(curve, name, display=True):
	curve3d = np.array([[p[0],p[1],0] for p in curve])
	ps_curves = ps.register_curve_network(name, curve3d, edges='line')
	ps_curves.set_radius(0.0025)
	ps_curves.set_enabled(display)

def visualize_samples(curve, name, display=True):
	curve3d = np.array([[p[0],p[1],0] for p in curve])
	ps_cloud = ps.register_point_cloud(name, curve3d)
	ps_cloud.set_radius(0.005)
	ps_cloud.set_enabled(display)

def visualize_sampled_curves(curves, name, display=True):
	for i in range(len(curves)):
		visualize_samples(curves[i], name + " points " + str(i), display)
		visualize_curve(curves[i], name + " " + str(i), display)

def read_OBJ(filepath):
	'''
	Read an OBJ file. Probably only efficient for small meshes.

	Args:
		filepath: string

	Returns:
		vertices: |V| x 3 NumPy array
		faces: |F| x 3 integer-valued NumPy array
	'''
	vertices = []
	faces = []
	with open(filepath, 'r') as file:
		for line in file:
			parts = line.strip().split()
			if not parts:
				continue
			elif parts[0] == 'v':
				vertex = list(map(float, parts[1:4]))
				vertices.append(vertex)
			elif parts[0] == 'f':
				face = [int(p.split('/')[0]) - 1 for p in parts[1:]]
				faces.append(face)

	return np.array(vertices, dtype=np.float64), np.array(faces, dtype=np.int64)

def background_triangle_mesh(radius: float, resolution: int) -> tuple[np.ndarray, np.ndarray]:
	'''
	Build a triangle mesh of equilateral triangles, where the mesh lies in the XY-plane,
	has approximately the given radius (centered around the origin) and the given resolution.
	Resolution = approx. number of triangles in the radial direction.
	
	Args:
		radius: Approximate radius of the mesh
		resolution: Number of triangles in the radial direction (must be >= 1)
		
	Returns:
		vertices: NumPy array of shape (n_vertices, 3) containing vertex positions
		faces: NumPy array of shape (n_faces, 3) containing triangle face indices
	'''
	if resolution < 1:
		raise ValueError("Resolution must be at least 1.")
	
	# Side length of each equilateral triangle
	triangle_size = radius / resolution
	
	# Height of each equilateral triangle
	triangle_height = triangle_size * np.sqrt(3) / 2.0
	
	# Lists to store vertices and faces
	vertex_positions = []
	faces = []
	
	# Create a mapping to avoid duplicate vertices
	vertex_indices = {}
	
	# Create vertices in a hexagonal grid
	# We use axial coordinates (q,r) for the hexagonal grid
	for q in range(-resolution, resolution + 1):
		# Clamp indices so they don't go beyond the hex mesh bounds
		r_start = max(-resolution, -q - resolution)
		r_end = min(resolution, -q + resolution)
		
		for r in range(r_start, r_end + 1):
			# Convert from axial coordinates to Cartesian coordinates
			x = triangle_size * (3.0 / 2.0 * q)
			y = triangle_size * (np.sqrt(3) / 2.0 * q + np.sqrt(3) * r)
			
			# Add vertex
			vertex_positions.append([x, y, 0.0])
			vertex_indices[(q, r)] = len(vertex_positions) - 1
	
	# Create triangles
	for q in range(-resolution, resolution):
		r_start = max(-resolution, -q - resolution)
		r_end = min(resolution - 1, -q + resolution - 1)
		
		for r in range(r_start, r_end + 1):
			# Check if we're still inside the hexagon
			if abs(q) + abs(r) + abs(-q - r) <= 2 * resolution:
				
				# Triangle pointing up-right
				if ((q, r) in vertex_indices and 
					(q + 1, r) in vertex_indices and 
					(q, r + 1) in vertex_indices):
					faces.append([
						vertex_indices[(q, r)], 
						vertex_indices[(q + 1, r)], 
						vertex_indices[(q, r + 1)]
					])
				
				# Triangle pointing down-left
				if ((q + 1, r) in vertex_indices and 
					(q + 1, r + 1) in vertex_indices and 
					(q, r + 1) in vertex_indices):
					faces.append([
						vertex_indices[(q + 1, r)], 
						vertex_indices[(q + 1, r + 1)], 
						vertex_indices[(q, r + 1)]
					])
				
				# Triangle pointing down-right (the missing one)
				if ((q, r) in vertex_indices and 
					(q + 1, r - 1) in vertex_indices and 
					(q + 1, r) in vertex_indices):
					faces.append([
						vertex_indices[(q, r)], 
						vertex_indices[(q + 1, r - 1)], 
						vertex_indices[(q + 1, r)]
					])
	
	# Convert to NumPy arrays
	vertices = np.array(vertex_positions, dtype=np.float64)
	faces = np.array(faces, dtype=np.int32)
	
	return vertices, faces

class DemoSolver():
	'''
	Handles solving and visualization.
	'''

	def __init__(self, mesh_name):

		self.mesh_name = mesh_name
		self.curves = None
		self.original_curves = None

		self.original_vertices = None
		self.original_faces = None
		self.vertices = None
		self.faces = None
		self.target_vertices = 0

		self.epsilon = 0.02
		self.target_vertices = 0

	def callback1D(self):

		if self.curves == None:
			if psim.Button("Adaptive integration"):
				smooth_curve, sampled_curve = adaptive_integration(self.epsilon)
				visualize_curve(smooth_curve, "smooth curve", display=True)
				visualize_samples(sampled_curve, "curve samples", display=True)

				# Visualize background field.
				V, F = background_triangle_mesh(3., 32)
				ps.register_surface_mesh(self.mesh_name, V, F)
				E = electric_field(V)
				ps.get_surface_mesh(self.mesh_name).add_vector_quantity("electric field", E, enabled=True)

			_, self.epsilon = psim.InputFloat("Epsilon", self.epsilon)

		else:
			if psim.Button("Ramer-Douglas-Peucker simplify"):
				self.curves = rdp_simplify_curves(self.curves, self.epsilon)
				visualize_sampled_curves(self.curves, "simplified curve", display=True)

			_, self.epsilon = psim.InputFloat("Epsilon", self.epsilon)

			if psim.Button("Quadric error simplify"):
				self.curves = quadric_error_simplify_curves(self.curves, self.target_vertices)
				self.target_vertices = size(self.curves) // 2
				visualize_sampled_curves(self.curves, "simplified curve", display=True)

			changed, self.target_vertices = psim.InputInt("Target # of vertices", self.target_vertices)


			if psim.Button("Evaluate error"):
				plot_errors(self.curves)

			if psim.Button("Reset curve"):
				self.curves = copy.deepcopy(self.original_curves)
				self.target_vertices = size(self.curves) // 2
				visualize_sampled_curves(self.curves, "simplified curve", display=True)

	def callback2D(self):

		if psim.Button("Quadric error simplify"):
			t1 = time.time()
			self.vertices, self.faces = quadric_error_simplify_mesh(self.vertices, self.faces, self.target_vertices)
			t2 = time.time()
			print("Time (s): %f" %(t2-t1))
			ps.register_surface_mesh(self.mesh_name, self.vertices, self.faces)
			self.target_vertices = self.vertices.shape[0] // 2

		changed, self.target_vertices = psim.InputInt("Target # of vertices", self.target_vertices)

		if psim.Button("Reset mesh"):
			self.vertices = copy.deepcopy(self.original_vertices)
			self.faces = copy.deepcopy(self.original_faces)
			self.target_vertices = self.vertices.shape[0] // 2
			ps.register_surface_mesh(self.mesh_name, self.vertices, self.faces)

def main():

	parser = argparse.ArgumentParser("LOD")
	parser.add_argument("--i", help="A curve or mesh file.", type=str, required=False)
	args = parser.parse_args()

	ps.init()

	mesh_name = "mesh"
	demo_solver = DemoSolver(mesh_name)

	if args.i:
		filename = os.path.basename(args.i)
		mesh_name, ext = os.path.splitext(filename)
		demo_solver = DemoSolver(mesh_name)

		if (ext == ".l"):
			demo_solver.curves = read_curve(args.i)
			demo_solver.original_curves = read_curve(args.i)
			demo_solver.target_vertices = size(demo_solver.curves) // 2
			visualize_sampled_curves(demo_solver.original_curves, "original curve", display=False)
			visualize_sampled_curves(demo_solver.curves, "simplified curve", display=True)
			ps.set_user_callback(demo_solver.callback1D)
		else:
			demo_solver.vertices, demo_solver.faces = read_OBJ(args.i)
			demo_solver.original_vertices, demo_solver.original_faces = read_OBJ(args.i)
			demo_solver.target_vertices = demo_solver.vertices.shape[0] // 2
			ps_mesh = ps.register_surface_mesh(demo_solver.mesh_name, demo_solver.vertices, demo_solver.faces)
			ps.set_user_callback(demo_solver.callback2D)

	else:
		ps.set_user_callback(demo_solver.callback1D)

	ps.show()

if __name__ == '__main__':
	main()
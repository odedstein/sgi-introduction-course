import numpy as np

def optimal_location_and_cost(Qe):
    """
    Compute the optimal vertex location after a single edge removal and evaluate its cost (quadric error)

    Inputs:
        Qe: (4,4) edge quadric

    Outputs:
        v_optimal: (3,1) optimal vertex position
        quadric_error: scalar quadric error
    """

    # v'Qv = v'Av + 2b'v + c 
    A = Qe[:3,:3]
    b = -Qe[:3,3]
    c = Qe[3,3]

    # get some candidate vertex locations
    v_optimal = np.linalg.solve(A, b)
    quadric_error = (v_optimal @ A).dot(v_optimal) - 2 * b.dot(v_optimal) + c

    return v_optimal, quadric_error
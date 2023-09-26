from ortools.linear_solver import pywraplp


def solve():
    # Create the linear solver with the GLOP backend.
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        return

    # Create the variables x and y.
    x = solver.NumVar(0, 1, "x")
    y = solver.NumVar(0, 2, "y")

    print("Number of variables =", solver.NumVariables())

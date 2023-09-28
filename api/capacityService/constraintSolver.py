from ortools.sat.python import cp_model


def constraintsolve():
    A = [2, 3, 2, 3, 5]
    B = [3, 4, 2, 4, 2]

    model = cp_model.CpModel()

    # stripheight
    strip_height = model.NewIntVar(1, 1000000000, "strip_height")

    # variables for each rectangle if it is in the strip or not
    in_strip_vars = []
    rotated_in_strip_vars = []

    for i in range(len(A)):
        in_strip_vars.append(model.NewBoolVar(f"rectangle_{i}_in_strip"))
        rotated_in_strip_vars.append(
            model.NewBoolVar(f"rectangle_{i}_rotated_in_strip")
        )

        # Constraints
        model.Add(A[i] == strip_height).OnlyEnforceIf(in_strip_vars[i])
        model.Add(B[i] == strip_height).OnlyEnforceIf(rotated_in_strip_vars[i])

    # Objective function
    model.Maximize(sum(in_strip_vars) + sum(rotated_in_strip_vars))

    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = True
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        for i in range(len(A)):
            if solver.Value(in_strip_vars[i]) == 1:
                print(f"rectangle {i}: {A[i]} x {B[i]}")
            elif solver.Value(rotated_in_strip_vars[i]) == 1:
                print(f"rectangle (rotated) {i}: {B[i]} x {A[i]}")

    return f"rectangle {i}: {A[i]} x {B[i]}"

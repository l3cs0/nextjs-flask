#!/usr/bin/env python3
# Copyright 2010-2022 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Solves a binpacking problem using the CP-SAT solver."""


from ortools.sat.python import cp_model


def bin_packing_problem_sat():
    """Solves a bin-packing problem using the CP-SAT solver."""
    # Data.
    bin_capacity = 1000
    slack_capacity = 100
    num_bins = 30
    all_bins = range(num_bins)

    items = [
        (20, 6),
        (15, 6),
        (30, 4),
        (45, 3),
        (45, 5),
        (45, 7),
        (60, 2),
        (60, 8),
        (75, 6),
        (10, 4),
        (25, 5),
        (35, 2),
        (50, 6),
        (55, 4),
        (70, 3),
        (80, 7),
        (90, 5),
        (100, 8),
        (15, 2),
        (40, 7),
        (65, 3),
        (85, 6),
        (95, 4),
        (110, 2),
        (120, 8),
        (130, 5),
        (45, 2),
        (55, 8),
        (70, 4),
        (75, 3),
        (25, 2),
        (55, 6),
        (40, 5),
        (85, 7),
        (110, 4),
        (30, 3),
        (70, 8),
        (20, 5),
        (50, 2),
        (90, 6),
        (35, 4),
        (75, 7),
        (15, 3),
        (60, 4),
        (95, 2),
        (120, 5),
        (45, 6),
        (80, 3),
        (130, 8),
        (10, 7),
        (65, 2),
        (100, 4),
        (55, 5),
        (75, 8),
        (110, 3),
        (85, 2),
        (30, 7),
        (25, 4),
        (60, 5),
        (40, 8),
        (25, 2),
        (55, 6),
        (40, 5),
        (85, 7),
        (110, 4),
        (30, 3),
        (70, 8),
        (20, 5),
        (50, 2),
        (90, 6),
        (35, 4),
        (75, 7),
        (15, 3),
        (60, 4),
        (95, 2),
        (120, 5),
        (45, 6),
        (80, 3),
        (130, 8),
        (10, 7),
        (65, 2),
        (100, 4),
        (55, 5),
        (75, 8),
        (110, 3),
        (85, 2),
        (30, 7),
        (25, 4),
        (60, 5),
        (40, 8),
        (25, 2),
        (55, 6),
        (40, 5),
        (85, 7),
        (110, 4),
        (30, 3),
        (70, 8),
    ]
    num_items = len(items)
    all_items = range(num_items)

    # Model.
    model = cp_model.CpModel()

    # Main variables.
    x = {}
    for i in all_items:
        num_copies = items[i][1]
        for b in all_bins:
            x[(i, b)] = model.NewIntVar(0, num_copies, f"x[{i},{b}]")

    # Load variables.
    load = [model.NewIntVar(0, bin_capacity, f"load[{b}]") for b in all_bins]

    # Slack variables.
    slacks = [model.NewBoolVar(f"slack[{b}]") for b in all_bins]

    # Links load and x.
    for b in all_bins:
        model.Add(load[b] == sum(x[(i, b)] * items[i][0] for i in all_items))

    # Place all items.
    for i in all_items:
        model.Add(sum(x[(i, b)] for b in all_bins) == items[i][1])

    # Links load and slack through an equivalence relation.
    safe_capacity = bin_capacity - slack_capacity
    for b in all_bins:
        # slack[b] => load[b] <= safe_capacity.
        model.Add(load[b] <= safe_capacity).OnlyEnforceIf(slacks[b])
        # not(slack[b]) => load[b] > safe_capacity.
        model.Add(load[b] > safe_capacity).OnlyEnforceIf(slacks[b].Not())

    # Maximize sum of slacks.
    model.Maximize(sum(slacks))

    # Solves and prints out the solution.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    print(f"Solve status: {solver.StatusName(status)}")
    if status == cp_model.OPTIMAL:
        print(f"Optimal objective value: {solver.ObjectiveValue()}")
        return f"solved XXX \n Optimal objective value: {solver.ObjectiveValue()}"
    print("Statistics")
    print(f"  - conflicts : {solver.NumConflicts()}")
    print(f"  - branches  : {solver.NumBranches()}")
    print(f"  - wall time : {solver.WallTime()}s")
    return "fail"

import random
import time
import matplotlib.pyplot as plt
import numpy as np

def generate_points(n):
    return [(random.randint(0, 10000), random.randint(0, 10000)) for _ in range(n)]

def naive_algorithm(points):
    pareto = []
    for p in points:
        if all(not (q[0] > p[0] and q[1] > p[1]) for q in points):
            pareto.append(p)
    pareto.sort()
    return pareto

def divide_and_conquer(points):
    def merge(left, right):
        result = []
        max_y = -1
        for p in sorted(left + right, reverse=True):
            if p[1] > max_y:
                result.append(p)
                max_y = p[1]
        return sorted(result)

    def dac(points):
        if len(points) <= 1:
            return points
        mid = len(points) // 2
        left = dac(points[:mid])
        right = dac(points[mid:])
        return merge(left, right)

    points.sort()
    return dac(points)

def output_sensitive(points):
    points.sort(reverse=True)
    pareto = []
    max_y = -1
    for x, y in points:
        if y > max_y:
            pareto.append((x, y))
            max_y = y
    return sorted(pareto)

def sorted_input(points):
    pareto = []
    max_y = -1
    for x, y in reversed(points):
        if y > max_y:
            pareto.append((x, y))
            max_y = y
    return sorted(pareto)

def measure_time(algorithm, points, runs=3):
    total = 0
    for _ in range(runs):
        start = time.time()
        algorithm(points)
        total += time.time() - start
    return total / runs

sizes = [100, 500, 1000, 2559, 5000, 8000, 10000, 10**5]
algorithms = {
    "Naive O(nh)": naive_algorithm,
    "Divide & Conquer O(n log n)": divide_and_conquer,
    "Output-sensitive O(n log h)": output_sensitive,
    "Sorted Input O(n)": sorted_input
}

results = {name: [] for name in algorithms}

for n in sizes:
    points = generate_points(n)
    sorted_points = sorted(points)
    for name, algo in algorithms.items():
        input_data = sorted_points if name == "Sorted Input O(n)" else points
        t = measure_time(algo, input_data)
        results[name].append(t)

def normalize_curve(curve, scale):
    max_val = max(curve)
    return [scale * val / max_val for val in curve]

n_vals = np.array(sizes)
theoretical_curves = {
    "Naive O(nh)": normalize_curve(n_vals**2, max(results["Naive O(nh)"])),
    "Divide & Conquer O(n log n)": normalize_curve(n_vals * np.log2(n_vals), max(results["Divide & Conquer O(n log n)"])),
    "Output-sensitive O(n log h)": normalize_curve(n_vals * np.log2(np.sqrt(n_vals)), max(results["Output-sensitive O(n log h)"])),
    "Sorted Input O(n)": normalize_curve(n_vals, max(results["Sorted Input O(n)"]))
}

plt.figure(figsize=(10, 6))

# Experimental curves
for name, times in results.items():
    plt.plot(sizes, times, linestyle='-.', marker='o', label=f"{name} (Experimental)")

# Theoretical curves
for name, curve in theoretical_curves.items():
    plt.plot(sizes, curve, linestyle='--', label=f"{name} (Theoretical)")

plt.title("Staircase / Pareto-optimal Algorithms: Experimental vs Theoretical")
plt.xlabel("Input Size (n)")
plt.ylabel("Execution Time (seconds)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

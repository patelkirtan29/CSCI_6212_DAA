import time
import math
import numpy
import matplotlib.pyplot as plt
import pandas as pd

def pseudoCode(n):
    j = 2
    Sum = 0
    a = list(range(n+1))
    b = list(range(n+1))
    while j < n:
        k = 2
        while k < n:
            Sum += a[int(k)] * b[int(k)] 
            k = (k * math.sqrt(k)) 
            if k <= 1:  
                break
        j += j // 2 
    return Sum

# Theoretical Computation
def theoretical_time(n):
    if n <= 2:
        return 1
    # For Theoretical computation, it comes to O(logn(log(logn)))
    # Log to the base 10 is taken into cosideration
    return math.log10(n) * math.log10(math.log10(n))


nRange = [10, 50, 10**2, 10**3, 10**4, 10**5, 10**6, 10**7]
theoreticalTime = []
experimentalTime = []

# Experimental Computation
for n in nRange:
    theoreticalTime.append(theoretical_time(n))
    startTime = time.perf_counter_ns()
    pseudoCode(n)
    endTime = time.perf_counter_ns()
    experimentalTime.append((endTime - startTime) / 1e6)
# Normalization of Theoretical Values (scale to ms range)
theoretical_avg, experimental_avg = numpy.average(theoreticalTime), numpy.average(experimentalTime)
scaling_constant = experimental_avg / theoretical_avg
theoreticalTime = [theoreticalTime[i] * scaling_constant for i in range(len(theoreticalTime))]

# Result Table comparing Experimental and Theoretical Computations
results = pd.DataFrame({
    "n": nRange,
    "Theoretical (ms)": theoreticalTime,
    "Experimental (ms)": experimentalTime
})

print(results.to_string(index=False))

# Plotting
plt.figure(figsize=(6, 4))
plt.plot(nRange, theoreticalTime, label="Theoretical Time", marker='o')
plt.plot(nRange, experimentalTime, label="Experimental Time", marker='x')

plt.xscale('log')
plt.yscale('log')
plt.xlabel("n")
plt.ylabel("Time (ms)")
plt.title("Comparison of Theoretical and Experimental Time Complexity")
plt.legend()
plt.show()

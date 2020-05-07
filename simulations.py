import matplotlib.pyplot as plt
import numpy as np
import scipy.special as sp

from algorithms import COMP, DD, TestSet

# Set variables to produce graph
n = 500
k = 5
test_increment = 10
num_iterations = 1000

# Initialise test vector and data arrays
t = TestSet(n, k)
COMP_data = []
DD_data = []
tests = []

# Generate number of tests for x axis
i = 0
while i < n:
    i += test_increment
    tests.append(i)

# Compute counting bound (loop used to cast to int for large values)
x = np.arange(n)
y = np.zeros(n)
for i in range(0, n):
    y[i] = 2 ** i / sp.binom(n, k)

# For each number of tests, run each algorithm num_iterations times
for i in tests:
    print('Trying {} tests'.format(i))
    COMP_successes = 0
    DD_successes = 0
    for j in range(1, num_iterations + 1):
        if COMP(t, i).success:
            COMP_successes += 1
        if DD(t, i).success:
            DD_successes += 1
    COMP_data.append(COMP_successes/num_iterations)
    DD_data.append(DD_successes/num_iterations)

# Plot the data as a graph
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
plt.plot(tests, COMP_data, '-o', label="COMP")
plt.plot(tests, DD_data, '-o', label="DD")
ax1.set_xlabel("Number of tests")
ax1.set_ylabel("Success probability")
ax1.set_title(
    "Success probability after {} trials, n = {}, k = {}"
    .format(num_iterations, n, k))
plt.plot(x, y, label="counting bound")
ax1.set_ylim(0, 1)
plt.legend(loc="lower right")
fig1.set_size_inches(10, 6)
plt.savefig("n{}k{}".format(n, k), dpi=300)

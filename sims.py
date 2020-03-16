from group_testing import TestSet, COMP
import numpy as np
import matplotlib.pyplot as plt

lower_bound = 10
length_range = 50

results = np.zeros(length_range)

ns = range(lower_bound, length_range + lower_bound)

for n in ns:
    # Floor division, makes 10% of set defective
    k = n // 10
    t = TestSet(n, k)
    noTests = COMP(t).T
    results[n - lower_bound] = noTests

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.scatter(ns, results)
ax1.set_xlabel("n")
ax1.set_ylabel("num_tests")
ax1.set_title("Size of test array against number of tests with k = n/10")
ax1.plot(ns, ns)
plt.show()

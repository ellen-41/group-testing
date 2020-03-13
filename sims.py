from group_testing import TestSet, COMP
import numpy as np

lower_bound = 10
length_range = 10

results = np.zeros(length_range)

for n in range(lower_bound, length_range + lower_bound):
    # Floor division, makes 10% of set defective
    k = n // 10
    t = TestSet(n, k)
    noTests = COMP(t).T
    results[n - lower_bound] = noTests

print(results)

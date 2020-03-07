from group_testing import TestSet, COMP

for n in range(10, 20):
    # Floor division, makes 10% of set defective
    k = n // 10
    t = TestSet(n, k)
    COMP(test)

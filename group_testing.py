import numpy as np
import random


def generate_bin_array(n, p):
    '''Generate a random array of 1s and 0s, 1s appearing with probability p'''
    bin_array = []
    for i in range(1, n + 1):
        value = np.random.binomial(1, p)
        bin_array.append(value)
    return bin_array


class TestSet:
    '''Object representing a test set of size n with roughly k defectives'''
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.defective_prob = k/n
        self.create_array()

    def create_array(self):
        '''Generates the test set as an array of 1s and 0s based on the
            probability of an item being defective being k/n'''
        self.test_array = generate_bin_array(self.n, self.defective_prob)


class Algorithm:
    '''Represents a generic algorithm'''
    def __init__(self, TestSet):
        self.test_array = TestSet.test_array
        self.n = TestSet.n
        self.groups = []
        # Generate initial group
        self.choose_group()

    def choose_group(self):
        '''Randomly generates a group to test'''
        group = generate_bin_array(self.n, 0.5)
        self.groups.append(group)
        # What should this probability be? Random?
        print(group)


class COMP(Algorithm):
    '''Includes all items that do not appear in any negative test'''
    def __init__(self, TestSet):
        super().__init__(TestSet)

    def test_group(self):
        definitely_negative = []
        product = False
        for i in range(0, self.n + 1):
            if self.group[i]:
                product = product or self.test_array[i]
                if product:
                    break
                else:
                    definitely_negative.append(i)
        if product:
            definitely_negative = []


test = TestSet(7, 3)
print(test.test_array)
pool = COMP(test)

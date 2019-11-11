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
        self.k = TestSet.k
        self.groups = []
        # Generate initial group
        self.choose_group()

    def choose_group(self):
        '''Randomly generates a group to test'''
        group = generate_bin_array(self.n, 1/self.k)
        self.groups.append(group)
        print(group)


class COMP(Algorithm):
    '''Includes all items that do not appear in any negative test'''
    def __init__(self, TestSet):
        super().__init__(TestSet)
        definitely_negative = []
        T = 0
        for group in self.groups:
            # Add all the DNDs from this test without duplicates
            definitely_negative = list(
                    set(definitely_negative + self.test_group(group)))
            if len(definitely_negative) < self.k:
                self.choose_group()
            T += 1
        print('The set of defective items is: {}'.format(definitely_negative))
        print('The number of tests required was {}'.format(T))

    def test_group(self, group):
        definitely_negative = []
        product = False
        for i in range(0, self.n):
            if group[i]:
                product = (product or self.test_array[i])
                if not product:
                    definitely_negative.append(i)
        if product:
            definitely_negative = []
            print('Test was positive')
        else:
            print('Test was negative')
            print('Definitely not defective: {}'.format(definitely_negative))
        return definitely_negative


test = TestSet(7, 3)
print(test.test_array)
pool = COMP(test)

import numpy as np
import random


def generate_prob_array(n, p):
    '''Generate a random array of 1s and 0s, 1s appearing with probability p'''
    bin_array = []
    for i in range(1, n + 1):
        value = np.random.binomial(1, p)
        bin_array.append(value)
    return bin_array


def generate_combin_array(n, k):
    '''Generate a random array of 1s and 0s, with k 1s (fixed)'''
    bin_array = np.zeros(n)
    bin_array[:k] = 1
    np.random.shuffle(bin_array)
    return bin_array


def defectives_to_array(n, defective_items):
    '''Convert an array of defective indices into the original array'''
    bin_array = np.zeros(n)
    for defective in defective_items:
        bin_array[defective] = 1
    return bin_array


class TestSet:
    '''Object representing a test set of size n with exactly k defectives'''
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.create_array()

    def create_array(self):
        '''Generates the test set as an array of 1s and 0s'''
        self.test_array = generate_combin_array(self.n, self.k)


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
        group = generate_prob_array(self.n, 1/self.k)
        if group not in self.groups:
            # Ensures that the group has not been tested before
            self.groups.append(group)
            print(group)
        else:
            # If the group has been used before, we discard it
            self.choose_group()


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
            if len(definitely_negative) < (self.n - self.k):
                self.choose_group()
            T += 1
            if T == 50:
                print('More than 50 tests required')
                break
        print('The set of DND items is: {}'.format(definitely_negative))
        defective_items = self.return_defective_items(definitely_negative)
        output_array = defectives_to_array(self.n, defective_items)
        print('As such, the defective items are: {}'.format(defective_items))
        print('The number of tests required was {}\n'.format(T))
        print('Our outputted test array is: \n{}'.format(output_array))

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
            print('Test was positive\n')
        else:
            print('Test was negative')
            print('Definitely not defective: {}\n'.format(definitely_negative))
        return definitely_negative

    def return_defective_items(self, dnd_list):
        all_elements = list(range(0, self.n))
        defective_items = np.setdiff1d(all_elements, dnd_list)
        return defective_items


test = TestSet(10, 3)
print('The test set is:')
print(test.test_array)
print('... beginning testing ...\n')
pool = COMP(test)

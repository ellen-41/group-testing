import random
import numpy as np


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
        group = generate_prob_array(self.n, 1/(self.k + 1))
        if group in self.groups:
            # Ensures that the group has not been tested before
            self.choose_group()
        else:
            self.groups.append(group)

    def compare_output(self, input_array, output_array):
        '''Check if our Khat is the same as the original set'''
        if np.array_equal(input_array, output_array):
            return True
        else:
            return False


class COMP(Algorithm):
    '''Includes all items that do not appear in any negative test'''
    def __init__(self, TestSet, num_tests):
        super().__init__(TestSet)
        input_array = TestSet.test_array
        definitely_negative = []
        T = 0
        for group in self.groups:
            # Add all the DNDs from this test without duplicates
            definitely_negative = list(
                    set(definitely_negative + self.test_group(group)))
            if len(definitely_negative) < (self.n - self.k):
                self.choose_group()
            T += 1
            if T == num_tests:
                break
        possible_defectives = self.return_possible_defectives(
            definitely_negative)
        output_array = defectives_to_array(self.n, possible_defectives)
        self.success = self.compare_output(input_array, output_array)

    def test_group(self, group):
        '''Performs a single test and returns the indices of DND items'''
        definitely_negative = []
        product = False
        for i in range(0, self.n):
            if group[i]:
                product = (product or self.test_array[i])
                if not product:
                    definitely_negative.append(i)
        if product:
            definitely_negative = []
        return definitely_negative

    def return_possible_defectives(self, dnd_list):
        '''Remove DNDs from array of all items, leaving possible defectives'''
        all_elements = list(range(0, self.n))
        possible_defectives = np.setdiff1d(all_elements, dnd_list)
        return possible_defectives


class DD(Algorithm):
    '''Eliminates all DND items, leaving only possible defectives,
        and outputs any of these that are the only item in a positive test'''
    def __init__(self, TestSet, num_tests):
        super().__init__(TestSet)
        input_array = TestSet.test_array
        definitely_negative = []
        # Array to hold our estimate for the defective set
        k_dd = []
        T = 0
        for group in self.groups:
            # Add all the DNDs from this test without duplicates
            definitely_negative = list(
                    set(definitely_negative + self.test_group(group)))
            if len(definitely_negative) < (self.n - self.k):
                self.choose_group()
            T += 1
            if T == num_tests:
                break
        possible_defectives = self.return_possible_defectives(
            definitely_negative)
        for group in self.groups:
            '''If an item is PD and only appears in a single test,
                add it to our array of definite defectives'''
            num_pd = 0
            dd_item = 0
            for i in possible_defectives:
                if group[i] == 1:
                    num_pd += 1
                    dd_item = i
            if num_pd == 1:
                k_dd.append(dd_item)
        output_array = defectives_to_array(self.n, k_dd)
        self.success = self.compare_output(input_array, output_array)

    def test_group(self, group):
        '''Performs a single test and returns the indices of DND items'''
        definitely_negative = []
        product = False
        for i in range(0, self.n):
            if group[i]:
                product = (product or self.test_array[i])
                if not product:
                    definitely_negative.append(i)
        if product:
            definitely_negative = []
        return definitely_negative

    def return_possible_defectives(self, dnd_list):
        '''Remove DNDs from array of all items, leaving possible defectives'''
        all_elements = list(range(0, self.n))
        possible_defectives = np.setdiff1d(all_elements, dnd_list)
        return possible_defectives

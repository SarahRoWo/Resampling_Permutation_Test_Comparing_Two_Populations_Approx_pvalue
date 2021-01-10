""" Implements a permutation test, returning an approximate p-value.

This script implements a permutation test for comparing two
populations. This script randomly shuffles data from two
populations, then compares a test statistic (e.g. sum)
from the original data with the test statistic of the
randomly shuffled data.

This implementation is intended for cases in which it is impractical
to calculate the test statistic of every possible combination
of the data. In these cases, a random subset of all possible
combinations are used. The test statistic for each combination
of the data in this subset is compared to the test statistic of the
original data. An approximate p-value is then calculated.
random_combination(iterable, r) is the function used to generate
this random subset.

This script was used in Woldemariam et al., Genetics 213, 59 (2019).

For additional information on permutation tests for comparing
two populations, please refer to Good (2006). Link below:
https://link.springer.com/content/pdf/10.1007/0-8176-4444-X.pdf
"""

import matplotlib.pyplot as plt
import random

# Provide manually inputted data for each condition.
listA = # Input data (list or tuple) from experiment here.
listB = # Input data (list or tuple) from control experiment here.

def random_combination(iterable, r):
    """ Generates list or tuple of r random elements from iterable.

    This is a generator function (found on Stack Overflow)
    that is intended to be equivalent
    to choosing random selections (without repetition)
    from itertools.combinations(iterable, r).

    Parameters
    ----------
    iterable : list or tuple
        The list,tuple,etc. that we will choose r (int)
        random elements from.
    r : int
        r is 'k' from n choose k.

    Returns
    -------
    generator
        next(random_combination(iterable, r)) returns a tuple that
        contains a random combination of elements from iterable.

    References
    ----------
    https://stackoverflow.com/questions/22229796/choose-at-random-from-combinations
    """

    used_indices = set()
    pool = tuple(iterable)
    # n (int) is the length of listA+listB (int).
    n = len(pool)
    # We add the indices corresponding to listA to the used_indices
    # variable so we don't return the experimental list as a
    # re-shuffled one.
    listAindex = tuple([i for i in range(r)])
    used_indices.add(listAindex)

    while True:
        # The indices variable accounts for the possibility that
        # combinations may have been already generated;
        # if a specific combination has already been generated
        # and comes up again, this allows us to skip that combination
        # so it won't be ranked twice.
        indices = tuple(sorted(random.sample(range(n), r)))

        if indices not in used_indices:
            used_indices.add(indices)
        yield tuple(pool[i] for i in indices)

random_combination_generator = random_combination(listA+listB, len(listA))

referencevalue = sum(listA)
lessthan = 0
greaterthan = 0
equalto = 0
timesitsrun = 0

# This is how many rearrangements will be done; can change value to
# whatever is tenable.
howmanyrandomcombinations = 500000
plothowmanyx = set()

for i in range(howmanyrandomcombinations):
    currentcombination = next(random_combination_generator)
    x = sum(currentcombination)
    plothowmanyx.add(x)

    if x < referencevalue:
        lessthan += 1
    elif x > referencevalue:
        greaterthan += 1
    elif x == referencevalue:
        equalto += 1

    timesitsrun += 1
    if timesitsrun % 50000 == 0:
        print(timesitsrun)

# This plots a histogram to visualize spread.
plothowmanyxl = list(plothowmanyx)
num_bins = 100
n, bins, patches = plt.hist(plothowmanyxl,
                            num_bins,
                            facecolor='blue',
                            alpha=0.5)
plt.show()

approxpvalueoneside = (lessthan+1) / (lessthan+1+greaterthan)
approxpvalueotherside = (greaterthan+1) / (lessthan+1+greaterthan)

# Note the approximate p-value for each side.
print("If doing two sided test, account for the 'approx. p-value other side'")
print("combinations less than {} sum of slopes = {}" .format('listA', lessthan))
print("combinations greater than {} sum of slopes = {}" .format('listA', greaterthan))
print("combinations equal to {} sum of slopes = {}" .format('listA', equalto))
print("approx. p-value one side = {}" .format(approxpvalueoneside))
print("approx. p-value other side = {}" .format(approxpvalueotherside))

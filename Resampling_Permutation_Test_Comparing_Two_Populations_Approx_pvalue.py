%matplotlib inline

import numpy as np

import matplotlib.mlab as mlab

import matplotlib.pyplot as plt

import random

# Manually inputted data for each condition.

listA = # data from experiment (list)

listB = # data from experiment - control (list)

def random_combination(iterable, r):

    """

    random_combination(iterable, r)

    This is a generator function (found on Stack Overflow) that is intended to be equivalent

    to choosing random selections (without repetition) from itertools.combinations(iterable, r)

    iterable is the list,tuple,etc... that we will choose r (int) random elements from

    n is the length of listA + listB

    r is like 'k' from n choose k
    
    link: https://stackoverflow.com/questions/22229796/choose-at-random-from-combinations

    """

    used_indices = set()

    pool = tuple(iterable)

    n = len(pool)

    listAindex = tuple([i for i in range(r)]) # adding the indices corresponding to listA so we don't return the experimental list as a re-shuffled one

    used_indices.add(listAindex)

    while True:

        indices = tuple(sorted(random.sample(range(n), r))) # this accounts for the possibility that combinations may

        # have been already generated; if a specific combination

        # has already been generated and comes up again,

        # this allows us to skip that combination so it won't be

        # ranked twice.

        if indices not in used_indices:

            used_indices.add(indices)

        yield tuple(pool[i] for i in indices)

random_combination_generator = random_combination(listA+listB, len(listA))

referencevalue = sum(listA)

lessthan = 0

greaterthan = 0

equalto = 0

timesitsrun = 0

howmanyrandomcombinations = 500000 #this is how many rearrangements will be done; can change value to whatever is tenable.

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

plothowmanyxl = list(plothowmanyx)

num_bins = 100

n, bins, patches = plt.hist(plothowmanyxl, num_bins, facecolor='blue', alpha=0.5)

plt.show()

approxpvalueoneside = (lessthan + 1) / (lessthan + 1 + greaterthan)

approxpvalueotherside = (greaterthan + 1) / (lessthan + 1 + greaterthan)

# don't have an elegant way to do a two sided test right now so if it's relevant then look at the approximate p value for the other side.

print("Note that if doing two sided test, also account for the 'approximate p value other side'.")

print("combinations less than {} sum of slopes = {}" .format('listA', lessthan))

print("combinations greater than {} sum of slopes = {}" .format('listA', greaterthan))

print("combinations equal to {} sum of slopes = {}" .format('listA', equalto))

print("approximate p value one side = {}" .format(approxpvalueoneside))

print("approximate p value other side = {}" .format(approxpvalueotherside))

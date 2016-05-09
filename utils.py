import math

from constants import EARTH_RADIUS


def dist(p1, p2):
    ''' calculates distance from coordinates p1 and p2 '''
    # both array lat, lng

    dlat = p1[0] - p2[0]
    dlon = p2[1] - p2[1]

    a = math.sin(dlat / 2)**2 + math.cos(p1[0]) * math.cos(p2[0]) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = EARTH_RADIUS * c
    return distance


def find_closest(point, path):
    ''' finds the shortest distance from a point to a path '''
    return min([dist(p1, point) for p1 in path])


def gaussian(val1, val2, var):
    ''' gaussian similarity (1/ to get distance) '''
    return 1. / math.exp(-(val1-val2)**2 / (2*var))


def variance(values):
    ''' calculates variance of some values '''
    mean = sum(values) / len(values)
    return sum((mean - value) ** 2 for value in values) / len(values)

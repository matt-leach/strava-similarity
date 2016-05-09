import json
import math
import random

from constants import *
from clean import thin


def get_activities():
    ''' load up activities '''
    with open('activities_latlng.json') as f:
        activities = json.load(f)

    with open('all_acts.json') as f:
        full_activities = json.load(f)

    assert len(activities) == len(full_activities)

    acts = []
    for ix, a in enumerate(activities):
        try:
            acts.append({'path': a[0]['data'],
                         'name': full_activities[ix]['name'],
                         'distance': full_activities[ix]['distance'] / 1609.,
                         'speed': full_activities[ix]['average_speed'],
                         'type': full_activities[ix]['workout_type'],
                         'id': full_activities[ix]['id']})
        except:
            pass
    return acts


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


def route_similarity(route1, route2):
    ''' note this is not communtative '''
    closests = []
    if not route1 or not route2:
        return 100
    for point in route1:
        closests.append(find_closest(point, route2))
        if closests[-1] > 100:
            return sum(closests) / len(closests)

    return sum(closests) / len(closests)


def variance(values):
    ''' calculates variance of some values '''
    mean = sum(values) / len(values)
    return sum((mean - value) ** 2 for value in values) / len(values)


def gaussian(val1, val2, var):
    ''' gaussian similarity (1/ to get distance) '''
    return 1. / math.exp(-(val1-val2)**2 / (2*var))


def run_similarity(run1, run2, variances):
    ''' calculates run similarity '''
    if run1['type'] != run2['type']:
        return None

    dist = gaussian(math.sqrt(run1['distance']), math.sqrt(run2['distance']), variances['distance'])
    speed = gaussian(run1['speed'], run2['speed'], variances['speed'])
    return dist * speed


def get_top_3(activity, other_activities, variances):
    ''' finds the top 3 most similar activities '''
    quite_close = []
    for test_activity in other_activities:
        route_1 = route_similarity(activity['path'], test_activity['path'])
        route_2 = route_similarity(test_activity['path'], activity['path'])
        route_sim = route_1 + route_2  # combine by adding
        run_sim = run_similarity(activity, test_activity, variances)
        if run_sim is not None and run_sim < 2:  # eliminate any which aren't fairly close
            quite_close.append({'name': test_activity['name'], 'val': min(route_sim, run_sim*0.7)})

    similar = sorted(quite_close, key=lambda x: x['val'])  # sort by the value
    similar += [{'name': None} for ii in range(0, 3)]
    print activity['name'], similar[0]['name'], similar[1]['name'], similar[2]['name']


if __name__ == '__main__':
    acts = get_activities()
    acts = [thin(a) for a in acts]

    variances = dict()
    variances['distance'] = variance([math.sqrt(a['distance']) for a in acts])
    variances['speed'] = variance([a['speed'] for a in acts])

    for ix in range(17, 20):
        a = acts[ix]
        get_top_3(a, acts[0:ix] + acts[ix+1:], variances)

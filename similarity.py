import json
import math

from constants import *
from clean import thin


def get_activities():
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
                         'type': full_activities[ix]['workout_type']})
        except:
            pass
    return acts


def dist(p1, p2):
    # both array lat, lng

    dlat = p1[0] - p2[0]
    dlon = p2[1] - p2[1]

    a = math.sin(dlat / 2)**2 + math.cos(p1[0]) * math.cos(p2[0]) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = EARTH_RADIUS * c
    return distance


def find_closest(point, path):
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


def run_similarity(run1, run2):
    if run1['type'] != run2['type']:
        return 10
    return math.fabs(run1['distance'] - run2['distance']) * math.fabs(run1['speed'] - run2['speed'])


def get_top_3(activity, other_activities):
    ''' finds the top 3 most similar activities '''
    quite_close = []
    for test_activity in other_activities:
        route_1 = route_similarity(activity['path'], test_activity['path'])
        route_2 = route_similarity(test_activity['path'], activity['path'])
        route_sim = route_1 + route_2  # combine by adding
        run_sim = run_similarity(activity, test_activity)

        if run_sim < 1:  # eliminate any which aren't fairly close
            quite_close.append({'name': test_activity['name'], 'val': min(0.1*route_sim, run_sim)})

    similar = sorted(quite_close, key=lambda x: x['val'])  # sort by the value
    similar += [{'name': None} for ii in range(0, 3)]
    print activity['name'], similar[0]['name'], similar[1]['name'], similar[2]['name']



if __name__ == '__main__':
    acts = get_activities()
    acts = [thin(a) for a in acts]
    print 'we done this'
    for ix, a in enumerate(acts[0:10]):
        get_top_3(a, acts[ix+1:])

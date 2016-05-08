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
    for point in route1:
        closests.append(find_closest(point, route2))

    return sum(closests) / len(closests)


def run_similarity(run1, run2):
    if run1['type'] != run2['type']:
        return 10
    return math.fabs(run1['distance'] - run2['distance']) * math.fabs(run1['speed'] - run2['speed'])


if __name__ == '__main__':
    acts = get_activities()
    acts = [thin(a) for a in acts]
    for ix, a in enumerate(acts[0:10]):
        sims = []
        for a2 in acts[ix+1:]:
            if a['path'] and a2['path']:
                sim = route_similarity(a['path'], a2['path'])
                sim2 = route_similarity(a2['path'], a['path'])
                route_sim = sim + sim2
                run_sim = run_similarity(a, a2)
                if run_sim < 1:
                    sims.append([a2['name'], min(0.1*route_sim, run_sim)])
        sims = sorted(sims, key=lambda x: x[1])
        sims += [[None], [None], [None]]
        print a['name'], sims[0][0], sims[1][0], sims[2][0]

import json
import math
import random

from constants import *
from models import Activity
from utils import *


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
            acts.append(Activity(full_activities[ix], a[0]['data']))
        except:
            pass
    return acts


def get_top_3(activity, other_activities, variances):
    ''' finds the top 3 most similar activities '''
    quite_close = []
    for test_activity in other_activities:
        route_1 = activity.route_similarity(test_activity)
        route_2 = test_activity.route_similarity(activity)
        # route_1 = route_similarity(activity['path'], test_activity['path'])
        # route_2 = route_similarity(test_activity['path'], activity['path'])
        try:
            route_sim = route_1 + route_2  # combine by adding
        except:
            # May be None
            route_sim = 100
        run_sim = activity.run_similarity(test_activity, variances)
        if run_sim is not None and run_sim < 2:  # eliminate any which aren't fairly close
            def get_pace_str(speed):
                pace = 1. / speed * 1609 / 60
                return str(int(pace)) + ':' + str(int((pace-int(pace)) * 60))

            quite_close.append({'name': test_activity.name, 'val': min(route_sim, run_sim*0.7),
                                'path': test_activity.path, 'distance': round(test_activity.distance, 1),
                                'pace': get_pace_str(test_activity.speed),
                                'id': test_activity.id,
                                'type': route_sim < run_sim*0.7})

    similar = sorted(quite_close, key=lambda x: x['val'])  # sort by the value
    similar += [{'name': None} for ii in range(0, 3)]
    print activity.name, similar[0]['name'], similar[1]['name'], similar[2]['name']
    print similar[0]['type'], similar[1]['type'], similar[2]['type']
    # with open(activity['name'] + '.json', 'w') as f:
    #     activity = {'name': activity['name'],
    #                 'distance': round(activity['distance'], 1),
    #                 'pace': get_pace_str(activity['speed']),
    #                 'path': activity['path']}
    #     f.write(json.dumps([activity] + similar[0:3], indent=4))


if __name__ == '__main__':
    acts = get_activities()
    print len(acts)
    variances = dict()
    variances['distance'] = variance([math.sqrt(a.distance) for a in acts])
    variances['speed'] = variance([a.speed for a in acts])

    for ix in [50]:
        a = acts[ix]
        get_top_3(a, acts[0:ix] + acts[ix+1:], variances)

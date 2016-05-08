import json
import math

from settings import ALL_ACTS_JSON


def stats():
    ''' just a basic function to view statistics from the activities we have '''
    with open('all_acts.json') as f:
        activities = json.load(f)

    total_dist = 0
    for a in activities:
        if a['type'] != 'Run':
            continue
        total_dist += a['distance']
    print total_dist / 1609.0
    print len([a for a in activities if a.get('workout_type', None) == 1])


def hist():
    ''' get buckets for data '''
    buckets = {ii/2.: 0 for ii in range(-10, 20)}  # max run is 20
    distances = []
    with open('all_acts.json') as f:
        activities = json.load(f)

    total_dist = 0
    for a in activities:
        if a['type'] != 'Run':
            continue
        dist = a['distance'] / 1609.0
        distances.append(dist)
        buckets[round(dist**0.5 * 2) / 2] += 1
    for ii in range(-10, 20):
        print buckets[ii/2.]

    print sum(distances) / len(distances)
    mean = sum(distances) / len(distances)
    print sum((mean - value) ** 2 for value in distances) / len(distances)

if __name__ == '__main__':
    hist()

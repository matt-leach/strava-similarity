import json

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


if __name__ == '__main__':
    stats()

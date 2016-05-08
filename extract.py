import requests
import json

from secret import token as TOKEN
from constants import ALL_ACTS_JSON, LATLNG_ACTS_JSON
from clean import get_ids


class StravaRequestor():

    def __init__(self):
        self.params = {}
        self.params['access_token'] = TOKEN
        self.base_url = 'https://www.strava.com/api/v3/'

    def get_activity(self, activity_id):
        ''' gets the detailed activity json from the api '''
        r = request.get('{}{}{}'.format(self.base_url, 'activities/', activity_id),
                        params=self.params)
        data = r.json()
        return {'polyline': data['map']['polyline'],
                'distance': data['distance'] / 1609,
                'date': data['start_date_local']}

    def get_latlng(self, activity_id):
        ''' gets the lat-lng data from an activity '''
        r = requests.get('{}activities/{}/streams/latlng'.format(self.base_url, activity_id),
                         params=self.params)
        try:
            data = r.json()
        except:
            return {}
        return data

    def get_activities(self, limit=20):
        ''' gets the short activity details and dumps to file '''
        params = self.params.copy()  # we're editing this so make a copy
        params['per_page'] = min(limit, 200)
        params['page'] = 1
        total = 0
        activities = []
        while total < limit:
            params['page'] += 1
            total += params['per_page']
            r = requests.get('{}activities'.format(self.base_url), params=params)
            activities += r.json()

        activities = activities[0:limit]
        return activities


if __name__ == '__main__':
    client = StravaRequestor()
    activities = client.get_activities(limit=10)
    with open(ALL_ACTS_JSON, 'w') as f:
        f.write(json.dumps(activities, indent=4))

    ids = get_ids()
    ll_activites = []
    for a_id in ids:
        a = client.get_latlng(a_id)
        ll_activites.append(a)
    with open(LATLNG_ACTS_JSON, 'w') as f:
        f.write(json.dumps(ll_activites, indent=4))

from utils import *
from constants import FILTER_NUM, METERS_IN_MILE

RUNNING_MAX_DIST = 50


class Activity(object):
    def __init__(self, data, path=[]):
        '''
        data is a dictionary from the Strava API and hence includes distance,
        pace, etc.
        path is an array of latlng coordinates which can also be pulled from Strava
        but normally separately
        '''
        self.path = path
        self.distance = data['distance'] / METERS_IN_MILE
        self.name = data['name']
        self.speed = data['average_speed']
        self.type = data['workout_type']
        self.id = data['id']

        self.thin()

    def thin(self):
        ''' thins out the activity path '''
        new = []
        for ix, point in enumerate(self.path):
            if ix % FILTER_NUM == 0:
                new.append(point)
        self.path = new

    def route_similarity(self, other):
        '''
        Finds the average distance from self.path to other.path

        NB: Not commutative
        '''
        closest_distances = []
        if not self.path or not other.path:
            return None

        if dist(self.path[1], other.path[1]) > RUNNING_MAX_DIST:
            # If the two paths are obviously not close
            # return None as 50 miles away may as well be
            # 5000.
            return None

        for point in self.path:
            closest_distances.append(find_closest(point, other.path))
        return sum(closest_distances) / len(closest_distances)

    def run_similarity(self, other, variances):
        '''
        calculates run similarity between self and other.
        variances is a dict of the variances of the values we are using for all
        activities.
        '''
        if self.type != other.type:
            return None

        dist = gaussian(math.sqrt(self.distance), math.sqrt(other.distance), variances['distance'])
        speed = gaussian(self.speed, other.speed, variances['speed'])
        return dist * speed

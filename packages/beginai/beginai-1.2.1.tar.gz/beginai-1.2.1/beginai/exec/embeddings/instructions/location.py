from math import sin, cos, sqrt, atan2, radians

def compute_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


class DistanceFromField(object):
    def __init__(self):
        pass

    def apply(self, value, compare_to_field_value):
        return compute_distance(value.get("latitude"), value.get("longitude"),
            compare_to_field_value.get("latitude"), compare_to_field_value.get("longitude"))

class DistanceFromPoint(object):
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def apply(self, value):
        return compute_distance(value.get("latitude"), value.get("longitude"),
            self.latitude, self.longitude)

instructions_map = {
    "DistanceFromField": DistanceFromField,
    "DistanceFromPoint": DistanceFromPoint
}

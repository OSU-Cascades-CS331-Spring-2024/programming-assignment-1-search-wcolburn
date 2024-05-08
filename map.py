class Map:
    def __init__(self, cities=None):
        if cities is None:
            cities = []
        self.cities = cities
        self.distances = {}
        self.coordinates = {}

    def add_distance(self, city1, city2, distance):
        if city1 not in self.distances:
            self.distances[city1] = {}
        if city2 not in self.distances:
            self.distances[city2] = {}
        self.distances[city1][city2] = distance
        self.distances[city2][city1] = distance

    def get_distance(self, city1, city2):
        if city1 == city2:
            return 0
        return self.distances[city1][city2]

    def get_neighbors(self, city):
        return list(self.distances[city].keys())

    def add_city(self, city):
        self.cities.append(city)

class Map:
    def __init__(self, cities=None):
        if cities is None:
            cities = []
        self.cities = cities
        self.distances = {}

    def add_distance(self, city1, city2, distance):
        if city1.name not in self.distances:
            self.distances[city1.name] = {}
        if city2.name not in self.distances:
            self.distances[city2.name] = {}
        self.distances[city1.name][city2.name] = distance
        self.distances[city2.name][city1.name] = distance

    def get_distance(self, city1, city2):
        return self.distances[city1.name][city2.name]

    def get_neighbors(self, city):
        return list(self.distances[city.name].keys())

    def add_city(self, city):
        self.cities.append(city)

    def get_city(self, city_name):
        for city in self.cities:
            if city.name == city_name:
                return city

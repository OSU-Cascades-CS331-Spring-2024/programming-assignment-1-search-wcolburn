class Map:
    def __init__(self, cities=None):
        if cities is None:
            cities = []
        self.cities = cities
        self.distances = {}

    def add_distance(self, city1, city2, distance):
        # print(distance)
        self.distances[city1] = [city2, distance]
        self.distances[city2] = [city1, distance]

    def get_neighbors(self, city):
        neighbors = []
        for distance_pair in self.distances[city]:
            neighbors.append(distance_pair[0])
        return neighbors

    def add_city(self, city):
        self.cities.append(city)

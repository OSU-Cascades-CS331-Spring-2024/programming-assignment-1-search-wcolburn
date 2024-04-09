class Map:
    def __init__(self, cities):
        self.cities = cities
        self.distance = {}

        def add_distance(city1, city2, distance):
            self.distance[city1] = [city2, distance]
            self.distance[city2] = [city1, distance]

        def add_city(city):
            self.cities.append(city)

class Agent:
    def __init__(self):
        self.goal = None

    def bfs(self, map, city_a, city_b):
        self.goal = city_b
        queue = [city_a]  # Queue holds frontier - cities to be visited in FIFO order
        path = []
        visited = [city_a]
        num_expanded = 0  # Number of cities expanded by adding neighbors to frontier
        num_maintained = 1  # Number of cities that enter the frontier. Begins at 1 for city_a.
        while len(queue) > 0:
            city = queue.pop(0)
            path.append(city)
            # If current node is city_b, path is finished
            if city == self.goal:
                info = dict()
                info["explored"] = len(path)
                info["maintained"] = num_maintained
                info["expanded"] = num_expanded
                return path
            else:  # Else add any unexplored neighbors to queue
                for next_city in map.get_neighbors(city):
                    num_expanded += 1
                    if next_city not in visited:
                        visited.append(next_city)
                        queue.append(next_city)
                        num_maintained += 1

def expand(map, city):
    return map.get_neighbors(city)


def calculate_cost(map, path):
    cost = 0
    for i in range(len(path) - 1):
        city = path[i]
        next_city = path[i + 1]
        cost += map.get_distance(city, next_city)
    return cost


def create_path(parent_list, start, end):
    path = []
    current = end
    while current != start:
        path.insert(0, current)
        current = parent_list[current]
    path.insert(0, start)
    return path


class Agent:
    def __init__(self):
        self.goal = None

    def bfs(self, map, city_a, city_b):
        self.goal = city_b
        queue = [city_a]  # Queue holds frontier - cities to be visited in FIFO order
        parent = {}
        visited = [city_a]
        num_expanded = 0  # Number of cities expanded by adding neighbors to frontier
        num_maintained = 1  # Number of cities that enter the frontier. Begins at 1 for city_a.
        while len(queue) > 0:
            city = queue.pop(0)
            # If current node is city_b, path is finished
            if city == self.goal:
                info = dict()
                path = create_path(parent, city_a, city_b)
                info["path"] = path
                info["explored"] = len(visited)
                info["maintained"] = num_maintained
                info["expanded"] = num_expanded
                info["cost"] = calculate_cost(map, path)
                return info
            else:  # Else add any unexplored neighbors to queue
                for next_city in expand(map, city):
                    if next_city not in visited:
                        visited.append(next_city)
                        queue.append(next_city)
                        parent[next_city] = city
                        num_maintained += 1
                num_expanded += 1

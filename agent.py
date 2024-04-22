import math
from queue import PriorityQueue
from math import sqrt


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


def is_cycle(parents, city):
    path = []
    current = city
    while current in parents.keys():
        parent = parents[current]
        if parent in path:
            return True
        path.append(parent)
        current = parent
    return False


def get_parent(parents, city):
    if city not in parents.keys():
        return None
    else:
        return parents[city]


def in_priority_queue(queue, city):
    for element in queue.queue:
        if element[1] == city:
            return True
    return False


def get_cost(queue, city):
    for element in queue.queue:
        if element[1] == city:
            return element[0]
    return None


def replace_in_priority_queue(queue, city, new_cost):
    for element in queue.queue:
        if element[1] == city:
            queue.queue.remove(element)
            break
    queue.put((new_cost, city))


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
        return None

    def iterative_deepening_search(self, map, city_a, city_b):
        for depth in range(0, len(map.cities)):
            info = self.dls(map, city_a, city_b, depth)
            if info["path"] != "cutoff":
                return info

    def dls(self, map, city_a, city_b, depth):
        self.goal = city_b
        queue = [city_a]  # LIFO - Holds a city until it is fully explored
        parent = {}
        city_depth = {city_a: 0}
        info = dict()
        info["path"] = "failure"  # Failure until depth is exceeded or goal is found
        num_visited = 0
        num_expanded = 0  # Number of cities expanded by adding neighbors to frontier
        num_maintained = 1  # Number of cities that enter the frontier. Begins at 1 for city_a.
        while len(queue) > 0:
            city = queue.pop()
            num_visited += 1
            # If current node is city_b, path is finished
            if city == self.goal:
                path = create_path(parent, city_a, city_b)
                info["path"] = path
                info["explored"] = num_visited
                info["maintained"] = num_maintained
                info["expanded"] = num_expanded
                info["cost"] = calculate_cost(map, path)
                return info
            if city_depth[city] > depth:
                info["path"] = "cutoff"
                return info
            elif not is_cycle(parent, city):
                for next_city in expand(map, city):
                    if next_city != get_parent(parent, city) and next_city not in queue:
                        queue.append(next_city)
                        parent[next_city] = city
                        city_depth[next_city] = city_depth[city] + 1
                        num_maintained += 1
                num_expanded += 1
        return info

    def ucs(self, map, city_a, city_b):
        self.goal = city_b
        queue = PriorityQueue()  # Ordered first out by distance
        queue.put((0, city_a))
        parent = {}
        explored = []
        num_expanded = 0  # Number of cities expanded by adding neighbors to frontier
        num_maintained = 1  # Number of cities that enter the frontier. Begins at 1 for city_a.
        while not queue.empty():
            city_node = queue.get()
            cost = city_node[0]
            city = city_node[1]
            explored.append(city)
            if city == self.goal:
                info = dict()
                path = create_path(parent, city_a, city_b)
                info["path"] = path
                info["explored"] = len(explored)
                info["maintained"] = num_maintained
                info["expanded"] = num_expanded
                info["cost"] = calculate_cost(map, path)
                return info
            else:
                for next_city in expand(map, city):
                    next_city_cost = cost + map.get_distance(city, next_city)
                    if not in_priority_queue(queue, next_city) and next_city not in explored:
                        queue.put((next_city_cost, next_city))
                        parent[next_city] = city
                        num_maintained += 1
                    elif in_priority_queue(queue, next_city) and next_city_cost < get_cost(queue, next_city):
                        replace_in_priority_queue(queue, next_city, next_city_cost)
                        parent[next_city] = city
                num_expanded += 1

    def estimate_distance_to_goal(self, map, city):
        city_coords = map.coordinates[city]
        goal_coords = map.coordinates[self.goal]

        city_y = city_coords[0]
        city_x = city_coords[1]
        goal_y = goal_coords[0]
        goal_x = goal_coords[1]

        return math.sqrt((goal_x - city_x) ** 2 + (goal_y - city_y) ** 2)

    def astar(self, map, city_a, city_b):
        pass

from map import Map
import argparse


def create_map_from_file(file_name):
    file = open(file_name)
    text = file.read().replace('\n', ' ').split()
    new_map = Map()
    i = 0
    while i < len(text):
        city = text[i]
        new_map.add_city(city)
        i += 10  # Skip coordinates
        while text[i][0] == 'v' and text[i][1] == 'a':
            if text[i] == "va-":  # In case of line breaking
                i += 1
            next_city = text[i].replace('va-', '', 1)
            i += 1
            distance = int(text[i])
            new_map.add_distance(city, next_city, distance)
            i += 1
            if i >= len(text):
                break
    file.close()
    return new_map


def bfs(map, city_a, city_b):
    queue = [city_a]  # Queue holds frontier - cities to be visited in FIFO order
    path = []  # Holds the path we visit cities
    while len(queue) > 0:
        city = queue.pop(0)
        path.append(city)
        # If current node is city_b, path is finished
        if city == city_b:
            return path
        else:  # Else add any unexplored neighbors to queue
            for next_city in map.get_neighbors(city):
                queue.append(next_city)


def dls(map, city_a, city_b):
    pass


def ucs(map, city_a, city_b):
    pass


def astar(map, city_a, city_b):
    pass


def main(**kwargs):
    file_name = kwargs["file"]
    map = create_map_from_file(file_name)

    # calais = map.get_city("calais")
    # neighbors = map.get_neighbors(calais)
    # print(neighbors)

    if kwargs["A"] and kwargs["B"]:
        search_type = kwargs["search"]
        city_a = kwargs["A"]
        city_b = kwargs["B"]

        if search_type == "bfs":
            print(bfs(map, city_a, city_b))
        elif search_type == "dls":
            dls(map, city_a, city_b)
        elif search_type == "ucs":
            ucs(map, city_a, city_b)
        elif search_type == "astar":
            astar(map, city_a, city_b)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("-s", "--search", help="Search type", default="bfs", choices=("bfs", "dls", "ucs", "astar"))
    p.add_argument("-A", help="Initial city", required=False)
    p.add_argument("-B", help="End city", required=False)
    p.add_argument("-f", "--file", help="File to load map from", required=True)

    args = p.parse_args()
    main(**vars(args))

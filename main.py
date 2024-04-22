from map import Map
from agent import Agent
import argparse


def create_map_from_file(file_name):
    file = open(file_name)
    text = file.read().replace('\n', ' ').split()
    new_map = Map()
    i = 0
    while i < len(text):
        city = text[i]
        new_map.add_city(city)

        coords = []
        for _ in range(0, 8):  # Get coordinates for city
            i += 1
            coords.append(text[i])
        new_map.coordinates[city] = coords

        i += 2  # Skip to neighbors
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


def main(**kwargs):
    file_name = kwargs["file"]
    map = create_map_from_file(file_name)

    agent = Agent()

    if kwargs["A"] and kwargs["B"]:
        search_type = kwargs["search"]
        city_a = kwargs["A"]
        city_b = kwargs["B"]

        if search_type == "bfs":
            agent.bfs(map, city_a, city_b)
        elif search_type == "dls":
            agent.iterative_deepening_search(map, city_a, city_b)
        elif search_type == "ucs":
            agent.ucs(map, city_a, city_b)
        elif search_type == "astar":
            print(agent.astar(map, city_a, city_b))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("-s", "--search", help="Search type", default="bfs", choices=("bfs", "dls", "ucs", "astar"))
    p.add_argument("-A", help="Initial city", required=False)
    p.add_argument("-B", help="End city", required=False)
    p.add_argument("-f", "--file", help="File to load map from", required=True)

    args = p.parse_args()
    main(**vars(args))

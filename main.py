from map import Map
from agent import Agent
import argparse


def convert_dms_to_dd(coordinates):
    degrees = int(coordinates[0])
    minutes = int(coordinates[1])
    seconds = int(coordinates[2])
    direction = coordinates[3]

    dd = degrees + minutes/60 + seconds/3600
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd


def create_map_from_file(file_name):
    file = open(file_name)
    text = file.read().replace('\n', ' ').split()
    new_map = Map()
    i = 0
    while i < len(text):
        city = text[i]
        new_map.add_city(city)

        dms_longitude = []
        dms_latitude = []
        for _ in range(0, 4):  # Get longitude coordinates for city
            i += 1
            dms_longitude.append(text[i])
        for _ in range(0, 4):  # Get latitude coordinates for city
            i += 1
            dms_latitude.append(text[i])
        dd_longitude = convert_dms_to_dd(dms_longitude)
        dd_latitude = convert_dms_to_dd(dms_latitude)
        new_map.coordinates[city] = [dd_longitude, dd_latitude]

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
    file_name = kwargs["map"]
    map = create_map_from_file(file_name)

    agent = Agent()

    if kwargs["A"] and kwargs["B"]:
        search_type = kwargs["search"]
        city_a = kwargs["A"]
        city_b = kwargs["B"]

        result = dict()
        if search_type == "bfs":
            result = agent.bfs(map, city_a, city_b)
        elif search_type == "dls":
            result = agent.iterative_deepening_search(map, city_a, city_b)
        elif search_type == "ucs":
            result = agent.ucs(map, city_a, city_b)
        elif search_type == "astar":
            result = agent.astar(map, city_a, city_b)
        print("Path: ")
        print_path(result["path"])


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("-S", "--search", help="Search type", default="bfs", choices=("bfs", "dls", "ucs", "astar"))
    p.add_argument("-A", help="Initial city", required=False)
    p.add_argument("-B", help="End city", required=False)
    p.add_argument("-M", "--map", help="File to load map from", required=True)

    args = p.parse_args()
    main(**vars(args))

from city import City
from map import Map
import sys
import argparse

p = argparse.ArgumentParser()
p.add_argument("-s", "--search", help="Search type", default="bfs", choices=("bfs", "dls", "ucs", "astar"))
p.add_argument("-A", help="Initial city", required=False)
p.add_argument("-B", help="End city", required=False)
p.add_argument("-f", "--file", help="File to load map from", required=True)


def create_map_from_file(file_name):
    file = open(file_name)

    text = file.read().replace('\n', ' ').split()

    new_map = Map()

    i = 0
    while i < len(text):

        city_name = text[i]
        city = City(city_name)
        new_map.add_city(city)

        i += 10  # Skip coordinates

        while text[i][0] == 'v' and text[i][1] == 'a':
            if text[i] == "va-":  # In case of line breaking
                i += 1
            next_city_name = text[i].replace('va-', '', 1)
            next_city = City(next_city_name)
            i += 1
            distance = int(text[i])

            new_map.add_city(next_city)
            new_map.add_distance(city, next_city, distance)

            # print(next_city.name, distance)
            i += 1
            if i >= len(text):
                break
    file.close()
    return new_map


def main(**kwargs):
    file_name = kwargs["file"]
    map = create_map_from_file(file_name)
    for city in map.cities:
        print(city.name)


if __name__ == '__main__':
    args = p.parse_args()
    main(**vars(args))

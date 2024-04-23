from map import Map
from agent import Agent
import argparse
import sys
import os


def convert_dms_to_dd(coordinates):
    degrees = int(coordinates[0])
    minutes = int(coordinates[1])
    seconds = int(coordinates[2])
    direction = coordinates[3]

    dd = degrees + minutes / 60 + seconds / 3600
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd


def create_map_from_file(file_name):
    file = open(file_name)
    text = file.read().replace('\n', ' ').split()
    new_map = Map()
    i = 0
    while i < len(text):
        city = text[i].lower()
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
            next_city = text[i].replace('va-', '', 1).lower()
            i += 1
            distance = int(text[i])
            new_map.add_distance(city, next_city, distance)
            i += 1
            if i >= len(text):
                break
    file.close()
    return new_map


def print_path(path):
    print("Path: ", end="")
    for city in path:
        print(city, end="")
        if city != path[-1]:
            print(" --> ", end="")
        else:
            print()


def print_results(result):
    if result["path"] == "failure":
        print("Path failure")
        return
    print_path(result["path"])
    print("Total cost: " + str(result["cost"]))
    print("Number of nodes explored: " + str(result["explored"]))
    print("Number of nodes expanded: " + str(result["expanded"]))
    print("Number of nodes maintained: " + str(result["maintained"]))


def print_results_to_solution_file(results):
    # Source: https://www.blog.pythonlibrary.org/2016/06/16/python-101-redirecting-stdout/
    original = sys.stdout
    sys.stdout = open('solutions.txt', 'a')
    print("Solutions for traveling from", results[0]["path"][0], "to", results[0]["path"][-1])
    print("----------------------------------------------------")
    for i in range(0, 4):
        result = results[i]
        if i == 0:
            print("BFS:")
        elif i == 1:
            print("DLS:")
        elif i == 2:
            print("UCS:")
        else:
            print("AStar:")
        print_results(result)
        print()
    sys.stdout = original


def calc_averages(results):
    datas = []
    for search in results:
        data = {"name": search, "optimal": 0}
        s = results[search]

        total_explored = 0
        total_expanded = 0
        total_maintained = 0
        for result in s:
            if result["path"] == "failure":
                continue
            total_explored += result["explored"]
            total_expanded += result["expanded"]
            total_maintained += result["maintained"]
        data["explored"] = total_explored / len(s)
        data["expanded"] = total_expanded / len(s)
        data["maintained"] = total_maintained / len(s)
        datas.append(data)

    for i in range(0, len(results["bfs"])):  # Calculate number of times a search found the optimal solution
        bfs_cost = results["bfs"][i]["cost"]
        dls = results["dls"][i]
        if dls["path"] != "failure":
            dls_cost = dls["cost"]
        else:
            dls_cost = 10000000
        ucs_cost = results["ucs"][i]["cost"]
        astar_cost = results["astar"][i]["cost"]

        lowest_cost = min(bfs_cost, dls_cost, ucs_cost, astar_cost)
        if bfs_cost == lowest_cost:
            datas[0]["optimal"] += 1
        if dls_cost == lowest_cost:
            datas[1]["optimal"] += 1
        if ucs_cost == lowest_cost:
            datas[2]["optimal"] += 1
        if astar_cost == lowest_cost:
            datas[3]["optimal"] += 1
    return datas


def write_averages(averages):
    f = open('README.txt', 'w')
    for search in averages:
        f.write(search["name"].capitalize() + "\n")
        f.write("----\n")
        f.write("Average explored: " + str(search["explored"]) + "\n")
        f.write("Average expanded: " + str(search["expanded"]) + "\n")
        f.write("Average maintained: " + str(search["maintained"]) + "\n")
        f.write("Number of times it found the optimal solution: " + str(search["optimal"]) + "\n\n")
    f.close()


def main(**kwargs):
    file_name = kwargs["map"]
    map = create_map_from_file(file_name)

    agent = Agent()

    if kwargs["A"] and kwargs["B"]:  # If user specifies a start city and an end city
        search_type = kwargs["search"].lower()
        city_a = kwargs["A"].lower()
        city_b = kwargs["B"].lower()

        result = dict()
        if search_type == "bfs":
            result = agent.bfs(map, city_a, city_b)
        elif search_type == "dls":
            result = agent.iterative_deepening_search(map, city_a, city_b)
        elif search_type == "ucs":
            result = agent.ucs(map, city_a, city_b)
        elif search_type == "astar":
            result = agent.astar(map, city_a, city_b)
        print_results(result)
    else:  # Search over default 9 cities with each search method
        cities_to_search = [("brest", "nice"), ("montpellier", "calais"), ("strasbourg", "bordeaux"),
                            ("paris", "grenoble"), ("grenoble", "paris"), ("brest", "grenoble"), ("grenoble", "brest"),
                            ("nice", "nantes"), ("caen", "strasbourg")]
        results = {"bfs": [], "dls": [], "ucs": [], "astar": [], }

        if os.path.exists("solutions.txt"):
            os.remove("solutions.txt")

        for city_pair in cities_to_search:
            city_a = city_pair[0]
            city_b = city_pair[1]

            bfs_result = agent.bfs(map, city_a, city_b)
            results["bfs"].append(bfs_result)

            dls_result = agent.iterative_deepening_search(map, city_a, city_b)
            results["dls"].append(dls_result)

            ucs_result = agent.ucs(map, city_a, city_b)
            results["ucs"].append(ucs_result)

            astar_result = agent.astar(map, city_a, city_b)
            results["astar"].append(astar_result)

            print_results_to_solution_file([bfs_result, dls_result, ucs_result, astar_result])
        averages = calc_averages(results)
        write_averages(averages)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("-S", "--search", help="Search type", default="bfs", choices=("bfs", "dls", "ucs", "astar"))
    p.add_argument("-A", help="Initial city", required=False)
    p.add_argument("-B", help="End city", required=False)
    p.add_argument("-M", "--map", help="File to load map from", required=True)

    args = p.parse_args()
    main(**vars(args))

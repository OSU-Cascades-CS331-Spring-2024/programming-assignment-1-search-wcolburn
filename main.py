from city import City
from map import Map

file = open("france.txt")

text = file.read().replace('\n', ' ').split()

map = Map()

i = 0
city = ""
next_city = ""
distance = ""
while i < len(text):

    city_name = text[i]
    city = City(city_name)
    map.add_city(city)

    i += 10  # Skip coordinates

    while text[i][0] == 'v' and text[i][1] == 'a':
        if text[i] == "va-":  # In case of line breaking
            i += 1
        next_city_name = text[i].replace('va-', '', 1)
        next_city = City(next_city_name)
        i += 1
        distance = int(text[i])

        map.add_city(next_city)
        map.add_distance(city, next_city, distance)

        # print(next_city.name, distance)
        i += 1
        if i >= len(text):
            break

file.close()

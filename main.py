import json

file = open("france.txt")


text = file.read().replace('\n', ' ').split()
print(text)

i = 0
city = ""
next_city = ""
distance = ""
while i < len(text):
    city = text[i]
    print(city)
    i += 10

    while text[i][0] == 'v' and text[i][1] == 'a':
        if text[i] == "va-":
            i += 1
        next_city = text[i]
        i += 1
        distance = text[i]
        print(next_city, distance)
        i += 1
        if i >= len(text):
            break



file.close()

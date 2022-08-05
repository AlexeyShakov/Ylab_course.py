import itertools as it


def finding_the_shortest_way():
    n = int(input("Сколько точек Вы хотите ввести?\n"))

    # создадим список, где будем хранить кортежи координат
    points = [tuple([int(i) for i in input(
        "Введите координаты точек через пробел. Первая точка должна быть почтовым отделением\n").split(" ")]) \
              for i in range(n)]

    # находим всевозможные комбинации перемещений почтальона и сразу фильтруем те, которые не начинаются с почтового отделения
    combinations = [comb for comb in it.permutations(points, n) if comb[0] == points[0]]

    # создадим словарь и в него будем класть все комбинации и их суммарные длины
    dist_dict = dict()

    # найдем общее расстояние для каждой комбинации
    for comb in combinations:
        dist = 0
        for i in range(1, len(comb)):
            dist += ((comb[i][0] - comb[i - 1][0]) ** 2 + (comb[i][1] - comb[i - 1][1]) ** 2) ** 0.5

        dist += ((points[0][0] - comb[i][0]) ** 2 + (points[0][1] - comb[i][1]) ** 2) ** 0.5
        dist_dict[comb] = dist

    # найдем минимальное значение
    min_val = min(dist_dict.values())

    # найдем комбинации с наименьшим расстоянием. На случай, если у нас несколько таких маршрутов
    res = [k for k, v in dist_dict.items() if v == min_val]

    # найдем промежуточные расстояния между точками. Для этого заведем список списков, куда будем класть промежуточ. расстояния для каждой комбинации
    intermediate_dist = [[] * i for i in range(len(res))]

    # найдем промежуточные расстояния
    for j in range(len(res)):
        inter_dist = 0
        for i in range(1, len(res[j])):
            inter_dist += ((res[j][i][0] - res[j][i - 1][0]) ** 2 + (res[j][i][1] - res[j][i - 1][1]) ** 2) ** 0.5
            intermediate_dist[j].append(inter_dist)

    # выведем полученные результаты
    for i in range(len(res)):
        print(points[0], end=" ")
        for j in range(1, len(res[i])):
            print("->", res[i][j], intermediate_dist[i][j - 1], end=" ")
        print(f"-> {points[0]}[{min_val}] = {min_val}")
        print()


while True:
    finding_the_shortest_way()
    question = input("Хотите найти кратчайшее расстояние для других точек? Введите 'да' или 'нет'\n")
    if question.lower() == "да":
        finding_the_shortest_way()
    elif question.lower() == "нет":
        break
    else:
        print("Введите 'да' или 'нет'")
        continue

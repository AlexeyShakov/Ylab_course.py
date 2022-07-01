import itertools as it

# create destinations
points = {"Почтовое отделение": (0, 2),
          "Ул. Грибоедова, 104/25": (2, 5),
          "Ул. Бейкер стрит, 221б": (5, 2),
          "Ул. Большая Садовая, 302-бис": (6, 6),
          "Вечнозелёная Аллея, 742": (8, 3)}

# create all possible combinations and leave only those which begin with 'Почтовое отделение'
combinations =  [comb for comb in it.permutations(points.keys(), 5) if comb[0] == "Почтовое отделение"]

# we will put combinations and their distance value
dist_dict = dict()

for comb in combinations:
  dist = 0
  for i in range(1, len(comb)):
    dist += ((points.get(comb[i])[0] - points.get(comb[i-1])[0])**2 + (points.get(comb[i])[1] - points.get(comb[i-1])[1])**2)**0.5

  # As the postman has to return to the initial point, we need to add the distance to that
  dist += ((points.get("Почтовое отделение")[0] - points.get(comb[len(comb) - 1])[0])**2 + (points.get("Почтовое отделение")[1] - points.get(comb[len(comb) - 1])[1])**2)**0.5
  dist_dict[comb] = dist

# find the minimim value in dictionary
min_val = min(dist_dict.values())

# find keys with minimum values. Res is the list of tuples
res = [k for k, v in dist_dict.items() if v==min_val]

for comb in res:
  # we will put here all intermidiate distances between points
  intermediate_dist = []
  inter_dist = 0
  for i in range(1, len(comb)):
    inter_dist += ((points.get(comb[i])[0] - points.get(comb[i-1])[0])**2 + (points.get(comb[i])[1] - points.get(comb[i-1])[1])**2)**0.5
    intermediate_dist.append(inter_dist)
  print(f"{points[comb[0]]} -> {points[comb[1]]}[{intermediate_dist[0]}] -> {points[comb[2]]}[{intermediate_dist[1]}] -> {points[comb[3]]}[{intermediate_dist[2]}] -> {points[comb[4]]}[{intermediate_dist[3]}] -> {points[comb[0]]}[{min_val}] = {min_val}")
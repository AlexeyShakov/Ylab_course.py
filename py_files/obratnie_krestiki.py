import random

# создаем игральное поле
def making_board():

    for num in range(10):
        for i in range(10):
            print(str(board[num][i]).ljust(3), end=" ")
            # print("|" ,str(board[i + num * 10]).ljust(2), "|", end=" ")
        print()


# возможно, нужно выкидывать значения из списка, чтобы РАНДОМ не перебирал слишком много значений!!!!!!!!!!!!!!

# делаем функцию, которая выполняет шаг
def taking_step(input_value: str):

    while True:
        # проверим, что пользователь вводит корректное число
        answer = int(input("На какой номер поставить " +  input_value + "?\n"))
        if answer not in board:
            print("Вы ввели неверный номер, попробуйте еще раз")
            continue
        # смотрим, чтобы ячейка была свободна
        if str(board[answer - 1]) in "XO":
            print("Данная ячейка занята, сделайте новый выбор")
            continue
        board[answer - 1] = input_value
        break



""" найдем комбинации, когда мы проигрываем. Данные код можно запустить один раз и просто скопировать результат в отдельную переменную. Мы можем так сделать
потому что наш данные статичны и не изменяются от игры к игре
"""
def finding_lose_combs() -> list:

    # создадим лист, где будем хранить проигрышные комбинации
    lose_combs = []

    # найдем все горизонтальные комбинации
    for row in board:
      for element in range(len(row)):
        if element > 5:
          continue
        lose_combs.append(tuple(row[element:(element+5)]))

    # чтобы облегчить поиск вертикальных комбинаций, транспонируем матрицу. Для этого понадобится создать новую матрицу
    trans_matrix = [[0]*10 for i in range(10)]
    for i in range(len(board)):
      for j in range(len(board)):
        # переставляем элементы исходной матрицы
        trans_matrix[j][i] = board[i][j]

    # теперь находим все проигрышные вертикальные комбинации
    for row in trans_matrix:
      for element in range(len(row)):
        if element > 5:
          continue
        lose_combs.append(tuple(row[element:(element+5)]))

    # найдем все диагональные комбинации. Для этого сначала найдем все элементы на диагонале и положим их в список
    diagonals = [[] for i in range(2)]
    for i in range(len(board)):
        diagonals[0].append(board[i][i])
        diagonals[1].append(board[i][::-1][i])

    # найдем все проигрышные комбинации для главной и побочной диагонали
    for diagonal in diagonals:
        for j in range(len(diagonal)):
            if j > 5:
                continue
            lose_combs.append(tuple(diagonal[j:j + 5]))

    return lose_combs





# Нужно найти элементы на ПОБОЧНОЙ ДИАГОНАЛИ!!!!!

# создаем игральную доску
board = [[0]*10 for i in range(10)]
el = 0
for i in range(10):
    for j in range(10):
        board[i][j] = el + 1
        el += 1
# находим проигрышные комбинации
lose_combs = finding_lose_combs()
print(len(lose_combs))


# making_board()


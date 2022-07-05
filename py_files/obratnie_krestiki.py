import random

# создаем игральное поле
def making_field(field: list):

    for num in range(10):
        for i in range(10):
            print("|" ,str(field[i + num * 10]).ljust(2), "|", end=" ")
        print()


# делаем функцию, которая выполняет пользовательский шаг
def human_step(input_value: str, field: list, field_copy: list):

    while True:
        # проверим, что пользователь вводит корректное число
        answer = int(input("На какой номер поставить " +  input_value + "?\n"))
        if answer not in field:
            print("Вы ввели неверный номер или этот номер занят, попробуйте еще раз")
            continue
        field[answer - 1] = input_value
        # нужно, чтобы компьютер не делал слишком много повторных выборов. Поэтому удалем выбранный элемент из копии нашего игрового поля
        field_copy.remove(answer)
        break

# функция для выполнения шага компьютера
def computer_step(input_value: str, field: list, field_copy: list, lose_combs: list):

    """
    сделаем наш компьютер похитрее, дадим ему шанс не выбирать проигрышное значение,
    даже если есть варианты лучше
    """
    comp_counter = 0
    while comp_counter <= 5:
        # выбираем случайне число из списка
        number = random.choice(field_copy)
        field[number - 1] = input_value
        # проверяем, будет ли этот шаг проигрышным для компьютера
        loser = check_lose(field, lose_combs)
        if loser:
            field[number - 1] = number
            comp_counter += 1
            continue
        else:
            field_copy.remove(number)
            break
    print("Компьютер выбрал значение - ", number)


""" найдем комбинации проигрышные комбинации. Данные код можно запустить один раз и просто скопировать результат в отдельную переменную. Мы можем так сделать
потому что наш данные статичны и не изменяются от игры к игре
"""
def finding_lose_combs() -> list:

    # Для того, чтобы удобнее найти все проигрышные комбинации, создадим матрицу в качестве нашего поля
    board = [[0]*10 for i in range(10)]
    el = 0
    for i in range(10):
        for j in range(10):
            board[i][j] = el + 1
            el += 1

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

    # найдем все диагональные комбинации. Для этого сначала найдем все элементы на диагоналях и положим их в список
    diagonals = [[] for i in range(2)]
    for i in range(len(board)):
        # для главной диагонали
        diagonals[0].append(board[i][i])
        # для побочной
        diagonals[1].append(board[i][::-1][i])

    # найдем все проигрышные комбинации для главной и побочной диагонали
    for diagonal in diagonals:
        for j in range(len(diagonal)):
            if j > 5:
                continue
            lose_combs.append(tuple(diagonal[j:j + 5]))

    return lose_combs


# функция проверки на проигрышные комбинации
def check_lose(field: list, lose_combs: list) -> bool:
    for each in lose_combs:
        # мы вычитаем единицу, потому что в списках нумерация начинается с 0, следовательно элемент со значения "1" будет под нулевым индексом.
        if (field[each[0] - 1]) == (field[each[1] - 1]) == (field[each[2] - 1]) == (field[each[3] - 1]) == (field[each[4] - 1]):
            return True
    else:
        return False

# основная функция, где выполняется вся последовательность действий
def main():

    # создадим игровое поле
    field = list(range(1, 101))

    """ 
    из копии поля мы будем удалять ячейки, которые были выбраны пользователем или компьютером. 
    Это нужно для того, чтобы компьютер выбирал значения без повторений
    """
    field_copy = field.copy()

    # найдем все проигрышные комбинации
    lose_combs = finding_lose_combs()

    # flag == True означает, что первый ход делает пользователь, то есть крестиками
    flag = True
    while True:
        question = input("Вы хотите ходить первым? Введите 'да' или 'нет'\n")
        if question.lower() not in ["да", "нет"]:
            print("Вы ввели неправильное значение. Введите 'да' или 'нет'")
            continue
        elif question.lower() == "нет":
            flag = False
            break
        else:
            break

    # счетчик нужен для того, чтобы отслеживать, кто делает ход
    counter = 0
    while True:
        if flag == True:
            making_field(field)
            # первым ходит пользователь, следовательно вызываем соответствующую функцию
            if counter % 2 == 0:
                human_step("X", field, field_copy)
            else:
                computer_step("O", field, field_copy, lose_combs)
            # делаем проверку на проигрышные комбинации
            if counter > 7:
                loser = check_lose(field, lose_combs)
                if loser:
                    if counter % 2 == 0:
                        making_field(field)
                        print("Вы проиграли!")
                        break
                    else:
                        making_field(field)
                        print("Компьютер проиграл!")
                        break
        # второй вариант - flag == False, значит первым ходит компьютер
        else:
            making_field(field)
            # первым ходит компьютер
            if counter % 2 == 0:
                computer_step("X", field, field_copy, lose_combs)
            else:
                human_step("O", field, field_copy)
            # проверяем проигрышные комбинации
            if counter > 7:
                loser = check_lose(field, lose_combs)
                if loser:
                    if counter % 2 == 0:
                        making_field(field)
                        print("Компьютер проиграл!")
                        break
                    else:
                        making_field(field)
                        print("Вы проиграли!")
                        break
        counter +=1
        # условие для ничьи
        if counter > 99:
            making_field()
            print("Ничья")


main()
while True:
    repeat = input("Вы хотите сыграть еще раз? Введите 'да' или 'нет'\n")
    if repeat.lower() == "да":
        main()
    elif repeat.lower() == "нет":
        print("До скорых встреч!")
        break
    else:
        print("Вы ввели неправильное значение.")
        continue



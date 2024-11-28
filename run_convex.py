#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void

try:
    X_1 = float(input("Введите координату x первой точки прямоугольника: "))
    Y_1 = float(input("Введите координату y первой точки прямоугольника: "))
    X_2 = float(input("Введите координату x второй точки прямоугольника: "))
    Y_2 = float(input("Введите координату y второй точки прямоугольника: "))
    print()

except ValueError:
    print("Данные некорректны, выполнение программы завершено!")

else:
    figure = Void(R2Point(X_1, Y_1), R2Point(X_2, Y_2))

    try:
        while True:
            figure = figure.add(R2Point())
            print(
                f"Требуемая площадь = "
                f"{round(figure.return_necessary_area(), 14)}\n",
                f"Общий периметр = {round(figure.perimeter(), 14)}\n",
                f"Общая площадь = {round(figure.area(), 14)}\n")

    except (EOFError, KeyboardInterrupt, ValueError):
        print("\nВыполнение программы завершено!")

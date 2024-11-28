#!/usr/bin/env -S python3 -B

from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void, Point, Segment, Polygon


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


def continue_to_input():
    tk.root.quit()


setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)

try:
    X_1 = float(input("Введите координату x первой точки прямоугольника: "))
    Y_1 = float(input("Введите координату y первой точки прямоугольника: "))
    X_2 = float(input("Введите координату x второй точки прямоугольника: "))
    Y_2 = float(input("Введите координату y второй точки прямоугольника: "))
    print()

except ValueError:
    print("Данные некорректны, выполнение программы завершено!")

else:
    tk = TkDrawer()
    figure = Void(R2Point(X_1, Y_1), R2Point(X_2, Y_2))

    rectangle = Polygon(R2Point(X_1, Y_1), R2Point(X_2, Y_2),
                        R2Point(X_1, Y_2), R2Point(X_1, Y_1),
                        R2Point(X_2, Y_2))
    rectangle = rectangle.add(R2Point(X_2, Y_1))

    rectangle.draw(tk)

    try:
        while True:
            figure = figure.add(R2Point())
            tk.clean()
            rectangle.draw(tk)
            figure.draw(tk)

            print(
                f"Требуемая площадь = "
                f"{round(figure.return_necessary_area(), 14)}\n",
                f"Общий периметр = {round(figure.perimeter(), 14)}\n",
                f"Общая площадь = {round(figure.area(), 14)}\n")

    except (EOFError, KeyboardInterrupt, ValueError):
        print("\nВыполнение программы завершено!")
        tk.close()

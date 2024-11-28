from math import sqrt


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))

        if y is None:
            y = float(input("y -> "))

        self.x, self.y = x, y

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x <= b.x) or
                 (a.x >= self.x >= b.x)) and
                ((a.y <= self.y <= b.y) or
                 (a.y >= self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = round(R2Point.area(a, b, self), 14)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False


if __name__ == "__main__":  # pragma: no cover
    v = R2Point(1.0, 1.0)
    print(type(v), v.__dict__)
    print(v.dist(R2Point(1.0, 0.0)))
    n, m, k = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(n, m, k))

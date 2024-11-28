import unittest
from math import sqrt

from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


class TestVoid(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Void(self.first_point, self.second_point)

    # Нульугольник является фигурой
    def test_figure(self):
        self.assertIsInstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Void (нульугольник)
    def test_void(self):
        self.assertIsInstance(self.f, Void)

    # Периметр нульугольника нулевой
    def test_perimeter(self):
        self.assertEqual(self.f.perimeter(), 0.0)

    # Площадь нульугольника нулевая
    def test_area(self):
        self.assertEqual(self.f.return_necessary_area(), 0.0)

    # Общая площадь нульугольника нулевая
    def test_total_area(self):
        self.assertEqual(self.f.area(), 0.0)

    # При добавлении точки нульугольник превращается в одноугольник
    def test_add(self):
        self.assertIsInstance(self.f.add(R2Point(0.0, 0.0)), Point)


class TestPoint(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Point(R2Point(0.0, 0.0), self.first_point, self.second_point)

    # Одноугольник является фигурой
    def test_figure(self):
        self.assertIsInstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Point (одноугольник)
    def test_point(self):
        self.assertIsInstance(self.f, Point)

    # Периметр одноугольника нулевой
    def test_perimeter(self):
        self.assertEqual(self.f.perimeter(), 0.0)

    # Общая площадь одноугольника нулевая
    def test_total_area(self):
        self.assertEqual(self.f.area(), 0.0)

    # Площадь одноугольника нулевая
    def test_area(self):
        self.assertEqual(self.f.return_necessary_area(), 0.0)

    # При добавлении точки одноугольник может не измениться
    def test_add_1(self):
        self.assertIs(self.f.add(R2Point(0.0, 0.0)), self.f)

    # При добавлении точки одноугольник может превратиться в двуугольник
    def test_add_2(self):
        self.assertIsInstance(self.f.add(R2Point(1.0, 0.0)), Segment)


class TestSegment(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Segment(R2Point(0.0, 0.0), R2Point(1.0, 0.0),
                         self.first_point, self.second_point)

    # Двуугольник является фигурой
    def test_figure(self):
        self.assertIsInstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Segment (двуугольник)
    def test_segment(self):
        self.assertIsInstance(self.f, Segment)

    # Периметр двуугольника равен удвоенной длине отрезка
    def test_perimeter(self):
        self.assertAlmostEqual(self.f.perimeter(), 2.0)

    # Площадь двуугольника нулевая
    def test_total_area(self):
        self.assertEqual(self.f.area(), 0.0)

    # Площадь двуугольника нулевая
    def test_area(self):
        self.assertEqual(self.f.return_necessary_area(), 0.0)

    # При добавлении точки двуугольник может не измениться
    def test_add_1(self):
        self.assertIs(self.f.add(R2Point(0.5, 0.0)), self.f)

    # Он не изменяется в том случае, когда добавляемая точка совпадает
    # с одним из концов отрезка
    def test_add_2(self):
        self.assertIs(self.f.add(R2Point(0.0, 0.0)), self.f)

    # При добавлении точки правее двуугольник может превратиться в другой
    # двуугольник
    def test_add_3(self):
        self.assertIsInstance(self.f.add(R2Point(2.0, 0.0)), Segment)

    # При добавлении точки левее двуугольник может превратиться в другой
    # двуугольник
    def test_add_4(self):
        self.assertIsInstance(self.f.add(R2Point(-1.0, 0.0)), Segment)

    # При добавлении точки двуугольник может превратиться в треугольник
    def test_add_5(self):
        self.assertIsInstance(self.f.add(R2Point(0.0, 1.0)), Polygon)


class TestPolygon1(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(1.0, 2.0)
        self.b = R2Point(2.0, 2.0)
        self.c = R2Point(1.0, 3.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    # Многоугольник является фигурой
    def test_figure(self):
        self.assertIsInstance(self.f, Figure)

    # Конструктор порождает экземпляр класса Polygon (многоугольник)
    def test_polygon_1(self):
        self.assertIsInstance(self.f, Polygon)

    # Изменение порядка точек при создании объекта всё равно порождает Polygon
    def test_polygon_2(self):
        self.f = Polygon(self.b, self.a, self.c,
                         self.first_point, self.second_point)
        self.assertIsInstance(self.f, Polygon)

    # Изменение количества вершин многоугольника
    #   изначально их три
    def test_vertexes_1(self):
        self.assertEqual(self.f.points.size(), 3)

    #   добавление точки внутрь многоугольника не меняет их количества
    def test_vertexes_2(self):
        self.assertEqual(self.f.add(R2Point(0.1, 0.1)).points.size(), 3)

    #   добавление другой точки может изменить их количество
    def test_vertexes_3(self):
        self.assertEqual(self.f.add(R2Point(1.5, 1.0)).points.size(), 4)

    #   изменения выпуклой оболочки могут и уменьшать их количество
    def test_vertexes_4(self):
        d = R2Point(0.4, 1.0)
        e = R2Point(1.0, 0.4)
        f = R2Point(0.8, 0.9)
        g = R2Point(0.9, 0.8)
        self.assertEqual(self.f.add(d).add(e).add(f).add(g).points.size(), 4)
        self.assertEqual(self.f.add(R2Point(-2.0, -6.0)).points.size(), 3)

    # Изменение периметра многоугольника
    #   изначально он равен сумме длин сторон
    def test_perimeter_1(self):
        self.assertAlmostEqual(self.f.perimeter(), 2.0 + sqrt(2.0))

    #   добавление точки может его изменить
    def test_perimeter_2(self):
        self.assertAlmostEqual(self.f.add(R2Point(1.0, 1.0)).perimeter(),
                               4.82842712474619)

    # Изменение площади многоугольника
    #   изначально она равна (неориентированной) площади треугольника
    def test_total_area1(self):
        self.assertAlmostEqual(self.f.area(), 0.5)

    #   добавление точки может увеличить площадь
    def test_total_area2(self):
        self.assertAlmostEqual(self.f.add(R2Point(1.0, 1.0)).area(), 1.0)

    # Изменение площади многоугольника
    #   изначально она равна (неориентированной) площади треугольника
    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 0.5)

    #   добавление точки может увеличить площадь
    def test_area_2(self):
        self.assertAlmostEqual(self.f.add(R2Point(2.0, 3.0)
                                          ).return_necessary_area(), 1.0)


class TestArea1(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(1.0, 3.0)
        self.b = R2Point(4.0, 2.0)
        self.c = R2Point(3.0, 4.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 2.5)

    def test_area_2(self):
        self.f.add(R2Point(3.0, 7.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 5.6)

    def test_area_3(self):
        self.f.add(R2Point(3.0, 7.0))
        self.f.add(R2Point(1.0, 6.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 6.6)

    def test_area_4(self):
        self.f.add(R2Point(3.0, 7.0))
        self.f.add(R2Point(1.0, 6.0))
        self.f.add(R2Point(2.0, 5.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 6.6)

    def test_area_5(self):
        self.f.add(R2Point(3.0, 7.0))
        self.f.add(R2Point(1.0, 6.0))
        self.f.add(R2Point(2.0, 5.0))
        self.f.add(R2Point(-2.0, 5.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 9.6)

    def test_area_6(self):
        self.f.add(R2Point(3.0, 7.0))
        self.f.add(R2Point(1.0, 6.0))
        self.f.add(R2Point(2.0, 5.0))
        self.f.add(R2Point(-2.0, 5.0))
        self.f.add(R2Point(5.0, 7.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 11.4)

    def test_area_7(self):
        self.f.add(R2Point(3.0, 7.0))
        self.f.add(R2Point(1.0, 6.0))
        self.f.add(R2Point(2.0, 5.0))
        self.f.add(R2Point(-2.0, 5.0))
        self.f.add(R2Point(5.0, 7.0))
        self.f.add(R2Point(1.0, 0.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 19.35)

    def test_area_8(self):
        self.f.add(R2Point(3.0, 7.0))
        self.f.add(R2Point(1.0, 6.0))
        self.f.add(R2Point(2.0, 5.0))
        self.f.add(R2Point(-2.0, 5.0))
        self.f.add(R2Point(5.0, 7.0))
        self.f.add(R2Point(1.0, 0.0))
        self.f.add(R2Point(7.0, 1.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 23.2)

    def test_area_9(self):
        self.f.add(R2Point(3.0, 7.0))
        self.f.add(R2Point(1.0, 6.0))
        self.f.add(R2Point(2.0, 5.0))
        self.f.add(R2Point(-2.0, 5.0))
        self.f.add(R2Point(5.0, 7.0))
        self.f.add(R2Point(1.0, 0.0))
        self.f.add(R2Point(7.0, 1.0))
        self.f.add(R2Point(-1.0, 1.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 26.0)

    def test_area_10(self):
        self.f.add(R2Point(3.0, 7.0))
        self.f.add(R2Point(1.0, 6.0))
        self.f.add(R2Point(2.0, 5.0))
        self.f.add(R2Point(-2.0, 5.0))
        self.f.add(R2Point(5.0, 7.0))
        self.f.add(R2Point(1.0, 0.0))
        self.f.add(R2Point(7.0, 1.0))
        self.f.add(R2Point(-1.0, 1.0))
        self.f.add(R2Point(-2.0, 3.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 27.0)

    def test_area_11(self):
        self.f.add(R2Point(3.0, 7.0))
        self.f.add(R2Point(1.0, 6.0))
        self.f.add(R2Point(2.0, 5.0))
        self.f.add(R2Point(-2.0, 5.0))
        self.f.add(R2Point(5.0, 7.0))
        self.f.add(R2Point(1.0, 0.0))
        self.f.add(R2Point(7.0, 1.0))
        self.f.add(R2Point(-1.0, 1.0))
        self.f.add(R2Point(-2.0, 3.0))
        self.f.add(R2Point(-2.0, 2.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 27.5)

    def test_area_12(self):
        self.f.add(R2Point(3.0, 7.0))
        self.f.add(R2Point(1.0, 6.0))
        self.f.add(R2Point(2.0, 5.0))
        self.f.add(R2Point(-2.0, 5.0))
        self.f.add(R2Point(5.0, 7.0))
        self.f.add(R2Point(1.0, 0.0))
        self.f.add(R2Point(7.0, 1.0))
        self.f.add(R2Point(-1.0, 1.0))
        self.f.add(R2Point(-2.0, 3.0))
        self.f.add(R2Point(-2.0, 2.0))
        self.f.add(R2Point(-3.0, 0.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 28.0)

    def test_area_13(self):
        self.f.add(R2Point(3.0, 7.0))
        self.f.add(R2Point(1.0, 6.0))
        self.f.add(R2Point(2.0, 5.0))
        self.f.add(R2Point(-2.0, 5.0))
        self.f.add(R2Point(5.0, 7.0))
        self.f.add(R2Point(1.0, 0.0))
        self.f.add(R2Point(7.0, 1.0))
        self.f.add(R2Point(-1.0, 1.0))
        self.f.add(R2Point(-2.0, 3.0))
        self.f.add(R2Point(-2.0, 2.0))
        self.f.add(R2Point(-3.0, 0.0))
        self.f.add(R2Point(-2.0, 5.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 28.0)


class TestArea2(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(1.0, 3.0)
        self.b = R2Point(4.0, 3.0)
        self.c = R2Point(2.0, 5.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 3.0)

    def test_area_2(self):
        self.f.add(R2Point(-6.0, 2.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 8.8)

    def test_area_3(self):
        self.f.add(R2Point(-6.0, 2.0))
        self.f.add(R2Point(-8.0, 1.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 10.0)

    def test_area_4(self):
        self.f.add(R2Point(-6.0, 2.0))
        self.f.add(R2Point(-8.0, 1.0))
        self.f.add(R2Point(6.0, 8.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 14.8)

    def test_area_5(self):
        self.f.add(R2Point(-6.0, 2.0))
        self.f.add(R2Point(-8.0, 1.0))
        self.f.add(R2Point(6.0, 8.0))
        self.f.add(R2Point(5.0, 5.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 15.0)

    def test_area_6(self):
        self.f.add(R2Point(-6.0, 2.0))
        self.f.add(R2Point(-8.0, 1.0))
        self.f.add(R2Point(6.0, 8.0))
        self.f.add(R2Point(5.0, 5.0))
        self.f.add(R2Point(4.0, 9.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 16.0)

    def test_area_7(self):
        self.f.add(R2Point(-6.0, 2.0))
        self.f.add(R2Point(-8.0, 1.0))
        self.f.add(R2Point(6.0, 8.0))
        self.f.add(R2Point(5.0, 5.0))
        self.f.add(R2Point(4.0, 9.0))
        self.f.add(R2Point(-2.0, 0.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 21.0)

    def test_area_8(self):
        self.f.add(R2Point(-6.0, 2.0))
        self.f.add(R2Point(-8.0, 1.0))
        self.f.add(R2Point(6.0, 8.0))
        self.f.add(R2Point(5.0, 5.0))
        self.f.add(R2Point(4.0, 9.0))
        self.f.add(R2Point(-2.0, 0.0))
        self.f.add(R2Point(4.0, -2.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 27.6)

    def test_area_9(self):
        self.f.add(R2Point(-6.0, 2.0))
        self.f.add(R2Point(-8.0, 1.0))
        self.f.add(R2Point(6.0, 8.0))
        self.f.add(R2Point(5.0, 5.0))
        self.f.add(R2Point(4.0, 9.0))
        self.f.add(R2Point(-2.0, 0.0))
        self.f.add(R2Point(4.0, -2.0))
        self.f.add(R2Point(11.0, -3.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 28.0)

    def test_area_10(self):
        self.f.add(R2Point(-6.0, 2.0))
        self.f.add(R2Point(-8.0, 1.0))
        self.f.add(R2Point(6.0, 8.0))
        self.f.add(R2Point(5.0, 5.0))
        self.f.add(R2Point(4.0, 9.0))
        self.f.add(R2Point(-2.0, 0.0))
        self.f.add(R2Point(4.0, -2.0))
        self.f.add(R2Point(11.0, -3.0))
        self.f.add(R2Point(-2.0, 9.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 28.0)


class TestArea3(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(1.0, 3.0)
        self.b = R2Point(4.0, 3.0)
        self.c = R2Point(3.0, 7.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 4.5)

    def test_area_2(self):
        self.f.add(R2Point(-2.0, -3.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 9.5)

    def test_area_3(self):
        self.f.add(R2Point(-2.0, -3.0))
        self.f.add(R2Point(1.0, 9.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 15.5)

    def test_area_4(self):
        self.f.add(R2Point(1.0, 9.0))
        self.f.add(R2Point(-2.0, -3.0))
        self.f.add(R2Point(-9.0, 9.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 21.5)


class TestArea4(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(1.0, 3.0)
        self.b = R2Point(4.0, 3.0)
        self.c = R2Point(6.0, 7.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 4.5)


class TestArea5(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(-1.0, 2.0)
        self.b = R2Point(4.0, 2.0)
        self.c = R2Point(-4.0, 8.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 11.0)


class TestArea6(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(1.0, 4.0)
        self.b = R2Point(-3.0, -2.0)
        self.c = R2Point(5.0, 0.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 7.5)


class TestArea7(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(1.0, 4.0)
        self.b = R2Point(-3.0, -2.0)
        self.c = R2Point(9.0, 0.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 11.0)


class TestArea8(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(1.0, 4.0)
        self.b = R2Point(4.0, -5.0)
        self.c = R2Point(4.0, 7.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 10.0)

    def test_area_2(self):
        self.f.add(R2Point(-8.0, 3.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 24.0)

    def test_area_3(self):
        self.f.add(R2Point(-8.0, 3.0))
        self.f.add(R2Point(6.0, 5.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 28.0)


class TestArea9(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(0.0, 3.0)
        self.b = R2Point(-4.0, 4.0)
        self.c = R2Point(8.0, 7.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 7.0)


class TestArea10(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(-10.0, 7.0)
        self.b = R2Point(12.0, 7.0)
        self.c = R2Point(0.0, -4.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 28.0)


class TestArea11(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(8.0, 0.0)
        self.b = R2Point(0.0, 8.0)
        self.c = R2Point(-1.0, 6.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 4.75)


class TestArea12(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(1.0, 6.0)
        self.b = R2Point(6.0, 1.0)
        self.c = R2Point(7.0, 3.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 3.5)

    def test_area_2(self):
        self.f.add(R2Point(1.0, -1.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 15.0)

    def test_area_3(self):
        self.f.add(R2Point(1.0, -1.0))
        self.f.add(R2Point(-4.0, 4.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 26.45)


class TestArea13(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(8.0, 0.0)
        self.b = R2Point(-1.0, 6.0)
        self.c = R2Point(11.0, 2.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 5.25)


class TestArea14(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(-4.0, 0.0)
        self.b = R2Point(6.0, 0.0)
        self.c = R2Point(6.0, 10.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 23.5)


class TestArea15(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(2.0, 0.0)
        self.b = R2Point(-4.0, 0.0)
        self.c = R2Point(6.0, 10.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 16.3)

    def test_area_2(self):
        self.f.add(R2Point(6.0, 4.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 21.5)


class TestArea16(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(-1.0, 0.0)
        self.b = R2Point(5.0, 0.0)
        self.c = R2Point(2.0, 6.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 12.0)


class TestArea17(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(-7.0, 7.0)
        self.b = R2Point(7.0, 7.0)
        self.c = R2Point(-7.0, -7.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 20.0)

    def test_area_2(self):
        self.f.add(R2Point(7.0, -7.0))
        self.assertAlmostEqual(self.f.return_necessary_area(), 28.0)


class TestArea18(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(-10.0, -3.0)
        self.b = R2Point(0.0, 7.0)
        self.c = R2Point(8.0, 3.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 26.25)


class TestArea19(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(-4.0, 7.0)
        self.b = R2Point(3.0, 0.0)
        self.c = R2Point(6.0, 3.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 16.3)


class TestArea20(unittest.TestCase):

    # Инициализация (выполняется для каждого из тестов класса)
    def setUp(self):
        self.a = R2Point(-4.0, 7.0)
        self.b = R2Point(3.0, 0.0)
        self.c = R2Point(3.0, 7.0)

        self.first_point = R2Point(-2.0, 5.0)
        self.second_point = R2Point(5.0, 1.0)

        self.f = Polygon(self.a, self.b, self.c,
                         self.first_point, self.second_point)

    def test_area_1(self):
        self.assertAlmostEqual(self.f.return_necessary_area(), 12.0)

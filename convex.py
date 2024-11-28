import itertools

from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def __init__(self, first_point, second_point):
        self.first_point = first_point
        self.second_point = second_point

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def return_necessary_area(self):
        return 0.0


class Void(Figure):
    """ Hульугольник """

    def __init__(self, first_point, second_point):
        super().__init__(first_point, second_point)

    def add(self, p):
        return Point(p, self.first_point, self.second_point)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p, first_point, second_point):
        super().__init__(first_point, second_point)

        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(
            self.p, q, self.first_point, self.second_point)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q, first_point, second_point):
        super().__init__(first_point, second_point)

        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r,
                           self.first_point, self.second_point)

        elif r.is_inside(self.p, self.q):
            return self

        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q,
                           self.first_point, self.second_point)

        else:
            return Segment(self.p, r,
                           self.first_point, self.second_point)


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, first_point, second_point):
        super().__init__(first_point, second_point)

        self.points = Deq()
        self.points.push_first(b)

        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)

        else:
            self.points.push_last(a)
            self.points.push_first(c)

        third_point = R2Point(self.first_point.x, self.second_point.y)
        fourth_point = R2Point(self.second_point.x, self.first_point.y)
        self.tuple_of_points = (self.first_point, third_point,
                                self.second_point, fourth_point)

        self.necessary_area = 0.0
        self.necessary_area = self.calculate_necessary_area(a, b, c)
        self.total_perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self.total_area = abs(R2Point.area(a, b, c))

    def calculate_necessary_area(self, a, b, c):
        a_is_inside = a.is_inside(self.first_point, self.second_point)
        b_is_inside = b.is_inside(self.first_point, self.second_point)
        c_is_inside = c.is_inside(self.first_point, self.second_point)

        points_in_rectangle = a_is_inside + b_is_inside + c_is_inside

        if points_in_rectangle == 3:
            return abs(R2Point.area(a, b, c))

        elif points_in_rectangle == 2:
            outside_point, inside_point_1, inside_point_2 = \
                sorted([a, b, c], key=lambda this_point: this_point.is_inside(
                    self.first_point, self.second_point))

            intersection_1 = self.find_suitable_intersection(
                inside_point_1, outside_point
            )

            intersection_2 = self.find_suitable_intersection(
                inside_point_2, outside_point
            )

            if intersection_1.x == intersection_2.x or \
                    intersection_1.y == intersection_2.y:
                return abs(R2Point.area(a, b, c)) - \
                    abs(R2Point.area(
                        intersection_1, intersection_2,
                        outside_point))

            else:
                for point in self.tuple_of_points:
                    if intersection_1.x == point.x and \
                            intersection_2.y == point.y or \
                            intersection_2.x == point.x and \
                            intersection_1.y == point.y:
                        return abs(R2Point.area(a, b, c)) - \
                            abs(R2Point.area(point, intersection_1,
                                             outside_point)) - \
                            abs(R2Point.area(point, intersection_2,
                                             outside_point))

        elif points_in_rectangle == 1:
            outside_point_1, outside_point_2, inside_point = \
                sorted([a, b, c], key=lambda this_point: this_point.is_inside(
                    self.first_point, self.second_point))

            intersection_1 = self.find_suitable_intersection(
                inside_point, outside_point_1
            )

            intersection_2 = self.find_suitable_intersection(
                inside_point, outside_point_2
            )

            list_of_outside_intersections = self.find_suitable_intersection(
                outside_point_1, outside_point_2, both_are_outside=True
            )

            if len(list_of_outside_intersections) == 0:
                if intersection_1.x == intersection_2.x or \
                        intersection_1.y == intersection_2.y:
                    return abs(R2Point.area(inside_point,
                                            intersection_1,
                                            intersection_2))

                else:
                    for point in self.tuple_of_points:
                        if intersection_1.x == point.x and \
                                intersection_2.y == point.y or \
                                intersection_2.x == point.x and \
                                intersection_1.y == point.y:
                            return abs(R2Point.area(a, b, c)) - \
                                abs(R2Point.area(point, intersection_1,
                                                 outside_point_1)) - \
                                abs(R2Point.area(point, intersection_2,
                                                 outside_point_2)) - \
                                abs(R2Point.area(point, outside_point_1,
                                                 outside_point_2))

            else:
                return abs(R2Point.area(
                    outside_point_1,
                    outside_point_2,
                    inside_point)) - \
                    min(
                        abs(R2Point.area(
                            outside_point_1,
                            intersection_1,
                            list_of_outside_intersections[0]
                        )),
                        abs(R2Point.area(
                            outside_point_1,
                            intersection_1,
                            list_of_outside_intersections[1]
                        ))) - \
                    min(
                        abs(R2Point.area(
                            outside_point_2,
                            intersection_2,
                            list_of_outside_intersections[0]
                        )),
                        abs(R2Point.area(
                            outside_point_2,
                            intersection_2,
                            list_of_outside_intersections[1]
                        )))

        else:
            list_of_points_in_triangle = []
            list_of_points_not_in_triangle = []

            for i in range(4):
                if self.is_in_triangle(a, b, c, self.tuple_of_points[i]):
                    list_of_points_in_triangle.append(self.tuple_of_points[i])

                else:
                    list_of_points_not_in_triangle.append(
                        self.tuple_of_points[i])

            all_cases_of_intersections = tuple(
                itertools.combinations((a, b, c), 2))
            list_of_intersections = []

            for case in all_cases_of_intersections:
                list_of_intersections += self.find_suitable_intersection(
                    case[0], case[1], both_are_outside=True
                )

            if len(list_of_intersections) == 0:
                if len(list_of_points_in_triangle) == 4:
                    return abs(self.first_point.x - self.second_point.x *
                               self.first_point.y - self.second_point.y) - \
                        self.necessary_area

                return 0.0

            if len(list_of_intersections) in {2, 3}:
                if len(list_of_intersections) == 3:
                    time_list = []

                    for point in list_of_intersections:
                        if point not in time_list:
                            time_list.append(point)

                    list_of_intersections = time_list.copy()

                if len(list_of_points_in_triangle) == 3:
                    return abs((self.first_point.x - self.second_point.x) *
                               (self.first_point.y -
                               self.second_point.y)) - abs(
                        R2Point.area(
                            list_of_intersections[0],
                            list_of_intersections[1],
                            list_of_points_not_in_triangle[0])) - \
                        self.necessary_area

                if len(list_of_points_in_triangle) == 2:
                    if (list_of_intersections[1].x ==
                        list_of_points_in_triangle[0].x or
                        list_of_intersections[1].y ==
                        list_of_points_in_triangle[0].y) and \
                            list_of_intersections[1] not in \
                            list_of_points_in_triangle:
                        return self.count_area_of_quadrilateral(
                            list_of_intersections[0],
                            list_of_intersections[1],
                            list_of_points_in_triangle[1],
                            list_of_points_in_triangle[0]
                        )

                    return self.count_area_of_quadrilateral(
                            list_of_intersections[0],
                            list_of_intersections[1],
                            list_of_points_in_triangle[0],
                            list_of_points_in_triangle[1]
                        )

                if len(list_of_points_in_triangle) == 1:
                    return abs(R2Point.area(
                        list_of_intersections[0], list_of_intersections[1],
                        list_of_points_in_triangle[0]))

            if len(list_of_intersections) in {4, 5} or any(
                    point_1 in self.tuple_of_points and
                    point_2 in self.tuple_of_points and point_1 != point_2
                    for point_1, point_2 in
                    itertools.combinations(list_of_intersections, 2)):
                if len(list_of_intersections) in {5, 6}:
                    time_list = []

                    for point in list_of_intersections:
                        if point not in time_list:
                            time_list.append(point)

                    list_of_intersections = time_list.copy()

                if len(list_of_points_in_triangle) == 0:
                    for i, j in itertools.combinations(range(4), 2):
                        list_of_numbers = [0, 1, 2, 3]

                        if list_of_intersections[i].x == \
                                list_of_intersections[j].x or \
                                list_of_intersections[i].y == \
                                list_of_intersections[j].y:
                            list_of_numbers.remove(i)
                            list_of_numbers.remove(j)

                            return self.count_area_of_quadrilateral(
                                list_of_intersections[i],
                                list_of_intersections[j],
                                list_of_intersections[list_of_numbers[0]],
                                list_of_intersections[list_of_numbers[1]]
                            )

                if len(list_of_points_in_triangle) in {1, 2}:
                    for i, j in itertools.combinations(range(4), 2):
                        list_of_numbers = [0, 1, 2, 3]

                        if list_of_intersections[i].x == \
                                list_of_points_in_triangle[0].x and \
                                list_of_intersections[j].y == \
                                list_of_points_in_triangle[0].y or \
                                list_of_intersections[i].y == \
                                list_of_points_in_triangle[0].y and \
                                list_of_intersections[j].x == \
                                list_of_points_in_triangle[0].x:
                            list_of_numbers.remove(i)
                            list_of_numbers.remove(j)

                            intermediate_area = abs(
                                R2Point.area(list_of_intersections[i],
                                             list_of_intersections[j],
                                             list_of_points_in_triangle[0]))

                            return self.count_area_of_quadrilateral(
                                list_of_intersections[i],
                                list_of_intersections[j],
                                list_of_intersections[list_of_numbers[0]],
                                list_of_intersections[list_of_numbers[1]]
                            ) + intermediate_area

            if len(list_of_intersections) in {6, 7}:
                intermediate_area = 0.0

                list_of_intersections_a_b = \
                    self.find_suitable_intersection(a, b,
                                                    both_are_outside=True)

                list_of_intersections_a_c = \
                    self.find_suitable_intersection(a, c,
                                                    both_are_outside=True)

                list_of_intersections_b_c = \
                    self.find_suitable_intersection(b, c,
                                                    both_are_outside=True)

                dictionary_of_intersections = {
                    'a_b': min(list_of_intersections_a_b[0],
                               list_of_intersections_a_b[1],
                               key=lambda necessary_point: R2Point.dist(
                                   necessary_point,
                                   a)),
                    'b_a': min(list_of_intersections_a_b[0],
                               list_of_intersections_a_b[1],
                               key=lambda necessary_point: R2Point.dist(
                                   necessary_point,
                                   b)),
                    'a_c': min(list_of_intersections_a_c[0],
                               list_of_intersections_a_c[1],
                               key=lambda necessary_point: R2Point.dist(
                                   necessary_point,
                                   a)),
                    'c_a': min(list_of_intersections_a_c[0],
                               list_of_intersections_a_c[1],
                               key=lambda necessary_point: R2Point.dist(
                                   necessary_point,
                                   c)),
                    'b_c': min(list_of_intersections_b_c[0],
                               list_of_intersections_b_c[1],
                               key=lambda necessary_point: R2Point.dist(
                                   necessary_point,
                                   b)),
                    'c_b': min(list_of_intersections_b_c[0],
                               list_of_intersections_b_c[1],
                               key=lambda necessary_point: R2Point.dist(
                                   necessary_point,
                                   c))}

                dictionary_of_points_of_triangle = {
                    'a': a, 'b': b, 'c': c
                }

                intermediate_area += abs(
                    R2Point.area(a, dictionary_of_intersections['a_b'],
                                 dictionary_of_intersections['a_c']))
                intermediate_area += abs(
                    R2Point.area(b, dictionary_of_intersections['b_a'],
                                 dictionary_of_intersections['b_c']))
                intermediate_area += abs(
                    R2Point.area(c, dictionary_of_intersections['c_a'],
                                 dictionary_of_intersections['c_b']))

                for necessary_pair in (
                        ('a_b', 'a_c'), ('b_a', 'b_c'), ('c_a', 'c_b')
                ):
                    if not (dictionary_of_intersections[necessary_pair[0]].x ==
                            dictionary_of_intersections[necessary_pair[1]].x or
                            dictionary_of_intersections[necessary_pair[0]].y ==
                            dictionary_of_intersections[necessary_pair[1]].y):
                        for point in self.tuple_of_points:
                            if self.is_in_triangle(
                                    dictionary_of_intersections[
                                        necessary_pair[0]],
                                    dictionary_of_intersections[
                                        necessary_pair[1]],
                                    dictionary_of_points_of_triangle[
                                        necessary_pair[0][0]], point) and \
                                    R2Point.area(
                                        dictionary_of_intersections[
                                            necessary_pair[0]],
                                        dictionary_of_intersections[
                                            necessary_pair[1]], point) != 0.0:
                                intermediate_area -= abs(R2Point.area(
                                    point,
                                    dictionary_of_intersections[
                                        necessary_pair[0]],
                                    dictionary_of_intersections[
                                        necessary_pair[1]]))

                return abs(R2Point.area(a, b, c)) - intermediate_area

    def find_suitable_intersection(self, probably_inside_point,
                                   outside_point, both_are_outside=False):
        list_of_intersection_points = []

        for i in range(4):
            intersection_point = self.find_intersection(
                probably_inside_point, outside_point,
                self.tuple_of_points[i], self.tuple_of_points[(i + 1) % 4])

            if intersection_point is not None and \
                    intersection_point.is_inside(probably_inside_point,
                                                 outside_point) and \
                    intersection_point.is_inside(self.first_point,
                                                 self.second_point):
                if both_are_outside:
                    list_of_intersection_points.append(intersection_point)

                else:
                    if probably_inside_point != intersection_point:
                        return intersection_point

            if not both_are_outside:
                list_of_intersection_points.append(intersection_point)

        if both_are_outside:
            return list_of_intersection_points

        elif probably_inside_point in list_of_intersection_points:
            return probably_inside_point

    @staticmethod
    def count_area_of_quadrilateral(point_on_first_axis_1,
                                    point_on_first_axis_2,
                                    point_on_second_axis_1,
                                    point_on_second_axis_2):
        return abs(R2Point.area(
            point_on_first_axis_1,
            point_on_first_axis_2,
            point_on_second_axis_1)) + \
            abs(R2Point.area(
                point_on_second_axis_1,
                point_on_second_axis_2,
                point_on_first_axis_2))

    @staticmethod
    def find_intersection(a, b, p, q):
        if b.y - a.y != 0:
            k = (b.x - a.x) / (a.y - b.y)
            sn = (p.x - q.x) + (p.y - q.y) * k

            if sn == 0:
                return

            fn = (p.x - a.x) + (p.y - a.y) * k
            n = fn / sn

        else:
            if p.y - q.y == 0:
                return

            n = (p.y - a.y) / (p.y - q.y)

        x = round(p.x + (q.x - p.x) * n, 14)
        y = round(p.y + (q.y - p.y) * n, 14)

        return R2Point(x, y)

    @staticmethod
    def is_in_triangle(point_1, point_2, point_3, necessary_point):
        triangle_area = abs(R2Point.area(point_1, point_2, point_3))

        sub_triangle_1 = abs(R2Point.area(necessary_point, point_1, point_2))
        sub_triangle_2 = abs(R2Point.area(necessary_point, point_1, point_3))
        sub_triangle_3 = abs(R2Point.area(necessary_point, point_2, point_3))

        return triangle_area == \
            sub_triangle_1 + sub_triangle_2 + sub_triangle_3

    def return_necessary_area(self):
        return self.necessary_area

    def perimeter(self):
        return self.total_perimeter

    def area(self):
        return self.total_area

    # добавление новой точки
    def add(self, t):
        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):
            # учёт удаления ребра, соединяющего конец и начало дека

            self.total_perimeter -= self.points.first().dist(
                self.points.last())

            self.total_area += abs(R2Point.area(t,
                                                self.points.last(),
                                                self.points.first()))

            self.necessary_area += self.calculate_necessary_area(
                t,
                self.points.last(),
                self.points.first())

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self.total_perimeter -= p.dist(self.points.first())
                self.total_area += abs(R2Point.area(t, p, self.points.first()))
                self.necessary_area += self.calculate_necessary_area(
                    t, p, self.points.first())
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self.total_perimeter -= p.dist(self.points.last())
                self.total_area += abs(R2Point.area(t, p, self.points.last()))
                self.necessary_area += self.calculate_necessary_area(
                    t, p, self.points.last())
                p = self.points.pop_last()
            self.points.push_last(p)

            self.total_perimeter += t.dist(
                self.points.first()) + t.dist(self.points.last())
            self.points.push_first(t)

        return self


if __name__ == "__main__":  # pragma: no cover
    f = Void(R2Point(2.0, 1.0), R2Point(3.0, -1.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)

"""
Паттерн Прототип применяется для созданя нового объекта путем клонирования исходного
с последующей модификацией клона
"""
import copy
import sys

# 7 способов для создания новой точки Point


class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


def make_object(cls, *args, **kwargs):
    return cls(*args, **kwargs)


point1 = Point(1,2)

# Точки point2, point3, point4 создаются динамически,
# имя класса передаются в качестве параметра
point2 = eval("{}({}, {})".format("Point", 2, 4))  # Опасно

# point4 создается так же, как point3 только синтаксис более приятный
# благодаря globals()
point3 = getattr(sys.modules[__name__], "Point")(3, 6)
point4 = globals()["Point"](4, 8)
point5 = make_object(Point, 5, 100)

# применяется классический подход на основе прототипа
point6 = copy.deepcopy(point5)
point6.x = 6
point6.y = 12

# эффективнее клонирования
point7 = point1.__init__(7, 14)

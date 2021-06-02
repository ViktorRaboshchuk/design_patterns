"""

Паттерн Компоновщик позволяет единообразно обрабатывать объекты,
образующие иерархию, вне зависимости от того, содержат они другие объекты или нет.

Такие объекты называются составными.

В классическом решении составные объекты - как отдельные, так и коллекции -
имеют один и тот же базовый класс.
У составных и несоставных объектов обычно одини и те же основные методы, но
состаные объекты добавляют методы для поддержки добавления, удаления и
перебора дочерних объектов

В данном файле рассматривается классическое решение , которое основано на
наличии абстрактного базового класса, общего для всех видов объектов(составных и несоставных)


"""
import abc
import sys


def main():
    pencil = SimpleItem("Pencil", 0.40)
    ruler = SimpleItem("Ruler", 1.60)
    eraser = SimpleItem("Eraser", 0.20)
    pencil_set = CompositeItem("Pencil Set", pencil, ruler, eraser)
    box = SimpleItem("Box", 1.00)
    boxed_pencil_set = CompositeItem("Boxed Pencil Set", box, pencil_set)
    boxed_pencil_set.add(pencil)
    for item in (pencil, ruler, eraser, pencil_set, boxed_pencil_set):
        item.print()


class AbstractItem(metaclass=abc.ABCMeta):
    """
    1. Метод __iter__ отвечает за итерируемость подкласса.
    2. Поскольку абстрактній класс имеет по меньшей мере один абстрактній метод или свойство,
        создавать обїект класса AbstractItem нельзя
    """
    @property
    @abc.abstractmethod
    def composite(self):
        pass

    def __iter__(self):
        return iter([])


class SimpleItem(AbstractItem):
    def __init__(self, name, price=0.00):
        self.name = name
        self.price = price

    @property
    def composite(self):
        return False

    def print(self, indent="", file=sys.stdout):
        print("{}${:.2f} {}".format(indent, self.price, self.name),
              file=file)


class AbstractCompositeItem(AbstractItem):
    """
    Создать экземпляр класса невозможно, потому что он наследует абстрактное свойство composite,
    но не реализует его
    """
    def __init__(self, *items):
        self.children = []
        if items:
            self.add(*items)

    def add(self, first, *items):
        self.children.append(first)
        if items:
            self.children.extend(items)

    def remove(self, item):
        self.children.remove(item)

    def __iter__(self):
        return iter(self.children)


class CompositeItem(AbstractCompositeItem):
    def __init__(self, name, *items):
        super().__init__(*items)
        self.name = name

    @property
    def composite(self):
        return True

    @property
    def price(self):
        """
        for item in self : интерпретатор Python вызывает iter(self), чтобы получить
        итератор для self -> происходит вызов метода __iter__(), возвращающий итератор,
        указывающий на self.children
        """
        return sum(item.price for item in self)

    def print(self, indent="", file=sys.stdout):
        print("{}${:.2f} {}".format(indent, self.price, self.name),
              file=file)
        for child in self:
            child.print(indent + "      ")


if __name__ == "__main__":
    main()
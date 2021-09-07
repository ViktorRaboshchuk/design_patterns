"""
Паттерн одиночка применяется, когда необходим класс, у которого должен быть
единственный экземпляр в своей программе

Самый простой способ получить функциональность одиночки - создать модуль с глобальными состоянимем,
которое хранится в закрытых переменных, и предоставить открытые функции для доступа к ним.
"""

import sqlite3


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    connection = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect("db.sqlite3")
            self.cursorobj = self.connection.cursor()
        return self.cursorobj


db1 = Database().connect()
db2 = Database().connect()
print("Database Objects DB1", db1)
print("Database Objects DB2", db2)


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance
s = Singleton()
print("Object created", s)
s1 = Singleton()
print("Object created", s1)

# Американская вилка
class UsaFork:
    def power_usa(self):
        print('power on. Usa')
# Европейская вилка
class EuroFork:
    def power_euro(self):
        print('power on. Euro')
# Американская розетка
class UsaSocket:
    def __init__(self, fork):
        self.fork = fork
    def connect(self):
        self.fork.power_usa()
# Вставляем американскую вилку в американскую розетку.
uf = UsaFork()
us = UsaSocket(uf)
us.connect()
# >>> power on. Usa
# # При попытке вставить европейскую вилку в американскую розетку, будет ошибка
# ef = EuroFork() 
# us = UsaSocket(ef) 
# us.connect() 
# # >>> AttributeError: 'EuroFork' object has no attribute 'power_usa'

class AdapterEuroInUsa:
    def __init__(self):
        self._euro_fork = EuroFork()
    def power_usa(self):
        self._euro_fork.power_euro()
        
# Вставляем американскую вилку в американскую розетку. 
uf = UsaFork() 
us = UsaSocket(uf) 
us.connect() 
# >>> power on. Usa
# Вставляем евро-адаптер в американскую розетку. 
ad = AdapterEuroInUsa()
us = UsaSocket(ad)
us.connect() 
# >>> power on. Euro

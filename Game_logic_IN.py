#Создаём класс исключений для поиска ошибок в ходе игры
class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Выстрел за пределы игрового поля!"

class BoardShotException(BoardException):
    def __str__(self):
        return "В эту клетку вы уже стреляли!"

class BoardShipException(BoardException):
    pass

#Создаём класс "Точка", в котором будем хранить наши координаты
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

#Создаём класс "Корабль", в котором будем хранить размер, направление и начало отрисовки корабля
class Ships:
    def __init__(self, bow, size, rotation):
        self.size = size                #Размер корабля
        self.hp = size                  #Количество жизней
        self.bow = bow                  #Начало отрисовки корабля
        self.rotation = rotation        #Положение корабля на доске

    @property
    def dots(self):
        ship_dots = []                  #Пустой список для хранения информации о корабле
        for i in range(self.size):
            new_x = self.bow.x          #Начало корабля по координате "х"
            new_y = self.bow.y          #Начало корабля по координате "у"

            if self.rotation == 0:
                new_x += i              #Направления корабля по "х"
            elif self.rotation == 1:
                new_y += i              #Направление корабля по "у"

            ship_dots.append(Dot(new_x, new_y))

        return ship_dots

#Создаём класс "Поле", в котором будем хранить наше игровое поле
class Field:
    def __init__(self, skip = False, size = 6):
        self.skip = skip                #Параметр, отвечающий за показ вражеской доски
        self.size = size                #Размер игрового поля
        self.field = [["◌"] * size for _ in range(size)] #Отрисовка игрового поля
        self.busy = []
        self.ships = []
        self.count = 0

#Создаём метод по отрисовке наших кораблей
    def add_ships(self, ships):
        for i in ships.dots:
            if self.out(i) or i in self.busy:
                raise BoardShipException() #Ошибка размещения корабля на поле
        for i in ships.dots:
            self.field[i.x][i.y] = "□"
            self.busy.append(i)

        self.ships.append(ships)
        self.contour(ships)

#Создаём метод по отрисовке контура вокруг корабля
    def contour(self, ships, verb = False):
        near = [(0, -1), (0, 0), (0, 1), (-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 0), (1, 1)]
        for i in ships.dots:
            for ix, iy in near:
                new = Dot(i.x + ix, i.y + iy)
                if not(self.out(new)) and new not in self.busy:
                    if verb:
                        self.field[new.x][new.y] = "•"
                    self.busy.append(new)

    def __str__(self):
        res = ""
        res += " |1|2|3|4|5|6|"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1}|" + "|".join(row) + "|"

        if self.skip:
            res = res.replace("□", "◌")
        return res

    def out(self, i):
        return not((0 <= i.x < self.size) and (0 <= i.y < self.size))

    def shoot(self, shot):
        if self.out(shot):
            raise BoardOutException()
        if shot in self.busy:
            raise BoardShotException()

        self.busy.append(shot)

        for i in self.ships:
            if shot in i.dots:
                i.hp -= 1
                self.field[shot.x][shot.y] = "x"
                if i.hp == 0:
                    self.count += 1
                    self.contour(i, verb=True)
                    print("Убит!")
                    return False
                else:
                    print("Ранил!")
                    return True

        self.field[shot.x][shot.y] = "•"
        print("Мимо!")
        return False

    def start(self):
        self.busy = []

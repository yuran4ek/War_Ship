from Game_logic_IN import BoardException, BoardShipException
from Game_logic_IN import Dot
from Game_logic_IN import Field
from Game_logic_IN import Ships
from random import randint

class Player:
    def __init__(self, field, enemy):
        self.field = field
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shoot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        i = Dot(randint(0, 5), randint(0, 5))
        print(f"Выстрел компьютера: {i.x + 1} {i.y + 1}")
        return i

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш выстрел: ").split()

            if len(cords) != 2:
                print("Неверный ввод! Введите только 2 координаты!")
                continue

            x, y = cords

            if not(x.isdigit()) or not(y.isdigit()):
                print("Неверный ввод! Вводите только числа!")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

class Game:
    def __init__(self, size = 6):
        self.size = size
        player = self.random_field()
        computer = self.random_field()
        computer.skip = True

        self.ai = AI(computer, player)
        self.user = User(player, computer)

    def random_field(self):
        field = None
        while field is None:
            field = self.random_ships()
        return field

    def random_ships(self):
        ship_len = [3, 2, 2, 1, 1, 1, 1]
        field = Field(size=self.size)
        count = 0
        for i in ship_len:
            while True:
                count += 1
                if count > 1000:
                    return None
                ship = Ships(Dot(randint(0, self.size), randint(0, self.size)), i, randint(0, 1))
                try:
                    field.add_ships(ship)
                    break
                except BoardShipException:
                    pass
        field.start()
        return field

    def greet(self):
        print("------------------------")
        print("Добро пожаловать в игру:")
        print("     'Морской бой'!     ")
        print("  Данная игра является  ")
        print(" консольной программой. ")
        print("В этой игре вы сразитесь")
        print(" против компьютера (ИИ) ")
        print("------------------------")
        print("      Правила игры:     ")
        print("Вводите в консоли только")
        print("две координаты в формате")
        print("         'x' 'y'        ")
        print(" где 'x' - номер строки ")
        print(" а 'y' - номер столбца  ")
        print("------------------------")
        print("         Удачи!         ")
        print("------------------------")

    def loop(self):
        count = 0
        while True:
            print("------------------------")
            print("Ваше поле: ")
            print(self.user.field)
            print("------------------------")
            print("Поле компьютера:")
            print(self.ai.field)

            if count % 2 == 0:
                print("------------------------")
                print("Ходит пользователь.")
                repeat = self.user.move()
            else:
                print("------------------------")
                print("Ходит компьютер.")
                repeat = self.ai.move()
            if repeat:
                count -= 1

            if self.ai.field.count == 7:
                print("------------------------")
                print(self.ai.field)
                print("Поздравляю, вы победили!")
                break

            if self.user.field.count == 7:
                print("------------------------")
                print(self.user.field)
                print("Увы, вы проиграли!")
                break
            count += 1

    def begin(self):
        self.greet()
        self.loop()








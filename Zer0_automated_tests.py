from abc import ABC


class Logger(ABC):
    def __init__(self, logger_name: str):
        self.logger_name = logger_name
        self._notes = []
        self._errors = []
        self._warnings = []
        self._msgs = []

    def add_error(self, new_error: str) -> None:
        self._errors += [new_error]

    def add_warning(self, new_warning: str) -> None:
        self._warnings += [new_warning]

    def add_note(self, new_note) -> None:
        self._notes += [new_note]

    def add_msg(self, new_msg) -> None:
        self._msgs += [new_msg]

    def print_one(self, anythings: list):
        if anythings:
            for one_msg in anythings:
                print(one_msg)

    def print_all(self) -> None:
        print(self.logger_name + ':')
        self.print_one(self._errors)
        self.print_one(self._warnings)
        self.print_one(self._notes)
        self.print_one(self._msgs)
        if not self._errors and \
                not self._warnings and \
                not self._notes:
            print('success!')
        print()

    def __del__(self):
        self.print_all()


class TestLogger(Logger):
    def UnknownVal(self):
        self.add_error("Неизвестный тип значения!")


class Card:
    def __init__(self, name="", vals=()):
        self.name = name
        # Упрощенный интерфейс: 
        # в тестах нам не требуется 
        # внутреннее разбиение значений на типы
        self.vals = list(vals)

    def add_usual_val(self, val):
        self.vals += [val]

    def add_selflink_val(self, val):
        self.vals += [val]

    def create_templ_card(self, refs):
        self.name = ""  # How refs -?-> name ???
        self.vals += [""]  # How rfs -?-> val ???
        return self

    def get(self):
        return f'\"{self.name}\": {self.vals}'

    def __str__(self):
        return self.get()


class Lib:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards += [card]

    def get(self):
        return self.cards

    def __str__(self):
        res = ""
        for one_card in self.cards:
            res += one_card.get()
        if res != "":
            res = "Cards:\n" + res
        return res


class Test:
    def __init__(self):
        self.loger = TestLogger("test_logger")
        self.cards = Lib()

    def add_usual_val(self):  # пока что без других условий (например, таких как depth)
        self.cards.add_card(Card("число", ["один", "два"]))

    def add_selflink_val(self):
        cards = self.cards.get()
        {
            True: lambda: cards[-1].add_selflink_val("число-число"),  # Пока что без доп. параметров тестов
            False: lambda: self.cards.add_card(Card("число", ["число-число"]))
        }[len(cards) > 0]()

    def add_templ_val(self):
        self.cards.add_card(Card().create_templ_card("число"))

    def generate_test(self, val_type):
        try:
            {
                "usual_val": self.add_usual_val,
                "selflink_val": self.add_selflink_val,
                "templ_val": self.add_templ_val
                # "id_val": self.add_is_val
            }[val_type]()
        except KeyError:
            self.loger.UnknownVal()
        return self

    def get(self):
        return self.cards  # пока что выводим только карты (1/3:+строки - входная, и выход с collisions!)

    def __str__(self):  # пока что выводим только карты (1/3:+строки - входная, и выход с collisions!)
        return f'{self.cards}\n'


class TestCombinator:
    def __init__(self):
        self.tests = []

    def add_test(self, test_type):
        new_test = Test().generate_test(test_type)
        self.tests += [new_test]
        if new_test.__str__() != "\n":
            print(new_test)

    def generate_all_tests(self):
        self.add_test("usual_val")
        self.add_test("selflink_val")
        self.add_test("templ_val")
        self.add_test("id_val")

    def print_all_tests(self):
        for one_test in self.tests:
            print(one_test)

    def __str__(self):
        res = ""
        for one_test in self.tests:
            res += one_test.__str__()
        return res


tests = TestCombinator()
tests.generate_all_tests()

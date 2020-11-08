from ui.menu import Menu

class Console:
    def __init__(self):
        self.__createMenu()

    def __createMenu(self):
        """
        Functia creaza meniul pentru utilizator
        """
        mainMenu = Menu()
        mainMenu.addItem("1. Adauga student")
        mainMenu.addItem("2. Iesire")
        Menu.initialize_stack(mainMenu)

    def __displayMenu(self):
        """
        Afiseaza meniul curent pentru utilizator
        """
        currentMenu = Menu.getCurrentMenu()
        currentMenu.printMenu()

    def __readOption(self):
        op = input("Alege o optiune: \n")
        return op


    def getNextOption(self, op):
        if Menu.user_exits(op):
            Menu.navigate_backwards()

    def run(self):
        self.__createMenu()

        while True:
            if Menu.getStackSize() == 0:
                return
            self.__displayMenu()
            op = self.__readOption()
            if Menu.getCurrentMenu().isOption(op):
                self.getNextOption(op)


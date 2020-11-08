
class Menu:
    """
    Clasa pentru reprezentarea unui meniu cu submeniuri si functionalitati
    """
    __menuStack = []
    __commands = {}

    def __init__(self, menuItems=None, menuFunctions = None, subMenus = None):
        if menuItems is None:
            menuItems = {}
        if menuFunctions is None:
            menuFunctions = {}
        if subMenus is None:
            subMenus = {}

        self.__menuItems = menuItems
        self.__menuFunctions = menuFunctions
        self.__subMenus = subMenus

    def getMenuItems(self):
        return self.__menuItems

    def get_menuFunctions(self):
        return self.__menuFunctions

    @staticmethod
    def get_commands():
        return Menu.__commands

    @staticmethod
    def set_commands(commands):
        Menu.__commands = commands

    def get_subMenus(self):
        return self.__subMenus

    def get_subMenuAt(self, key):
        return (self.get_subMenus())[key]

    def get_functionAt(self, functions, index):
        return functions[index]

    def printMenu(self):
        items = self.getMenuItems().values()
        print()
        for item in items:
            print(item)
        print()

    @staticmethod
    def user_exits(op):
        """
        Returneaza True daca optiunea aleasa de utilizator op indica iesirea din meniul curent.
        :param op: str - optiunea aleasa de utilizator
        :return True: utilizatorul iese din submeniu
        :return False: altfel
        """
        menuItems = Menu.getCurrentMenu().getMenuItems()
        if int(op) == len(menuItems.keys()):
            return True
        return False

    @staticmethod
    def navigate_backwards():
        if len(Menu.__menuStack) > 0:
            Menu.__menuStack.pop()

    @staticmethod
    def getCurrentMenu():
        currentMenu = Menu.__menuStack[len(Menu.__menuStack) - 1]
        return currentMenu

    @staticmethod
    def navigate_to_submenu(op):
        currentMenu = Menu.getCurrentMenu()
        Menu.__menuStack.append(currentMenu.get_subMenuAt(op))

    @staticmethod
    def __getMenuStack():
        return Menu.__menuStack


    @staticmethod
    def getStackSize():
        return len(Menu.__menuStack)

    @staticmethod
    def initialize_stack(mainMenu):
        if len(Menu.__menuStack) == 0:
            Menu.__menuStack.append(mainMenu)

    @staticmethod
    def get_commandAt(key):
        return Menu.__commands[key]

    def addItem(self, item):
        key = str(len(self.__menuItems)+1)
        self.__menuItems[key] = item

    def addFunction(self, function):
        key = str(len(self.__menuItems)+1)
        self.__menuFunctions[key] = function

    def addSubMenu(self, subMenu):
        key = str(len(self.__subMenus) + 1)
        self.__subMenus[key] = subMenu
        
    def isOption(self, op):
        """
        Verifica daca stringul op este o optiune valida in meniul curent
        :param op: string reprezentand optiunea
        :return True: daca op este optiune
        :return False: daca op nu este optiune 
        """
        if op in self.getMenuItems().keys():
            return True
        return False
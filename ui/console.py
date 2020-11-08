from ui.menu import Menu
from validation.errors import InvalidStudentError, StudentAlreadyExistsError

class Console:
    def __init__(self, studentSrv):
        self.__createMenu()
        self.__studentSrv = studentSrv

    def __createMenu(self):
        """
        Functia creaza meniul pentru utilizator
        """
        addStudentMenu = Menu()
        addStudentMenu.addItem("1. Adauga un student in lista")
        addStudentMenu.addFunction(self.addStudent)
        addStudentMenu.addItem("2. Inapoi...")

        mainMenu = Menu()
        mainMenu.addItem("1. Adauga student")
        mainMenu.addItem("2. Iesire")
        mainMenu.addSubMenu(addStudentMenu)
        Menu.initializeStack(mainMenu)

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
        if Menu.userExits(op):
            Menu.navigateBackwards()
            return
        currentMenu = Menu.getCurrentMenu()

        if op in currentMenu.getSubMenus().keys():
            Menu.navigateToSubmenu(op)
            return

        function = currentMenu.getFunction(op)
        function()

    def addStudent(self):
        """
        Ia datele corespunzatoare de la utilizator si le trimite serviciului pentru adaugare
        student in lista
        """
        firstName = input("Dati prenumele studentului: \n").strip()
        lastName = input("Dati numele studentului: \n").strip()
        IDStudent = input("Dati ID-ul studentului: \n").strip()
        print()

        try:
            self.__studentSrv.addStudent(IDStudent, firstName, lastName)
        except InvalidStudentError as err:
            print(str(err))
        except StudentAlreadyExistsError as err:
            print(str(err))
        else:
            self.printStudents()
            input("Apasati Enter pentru a continua...\n")

    def printStudents(self):
        students = self.__studentSrv.getStudents()
        print("Studentii din cadrul facultatii: \n")
        for student in students:
            print("ID: " + student.getID())
            print("Nume: " + student.getLastName())
            print("Prenume: " + student.getFirstName())
            print()


    def run(self):

        while True:
            if Menu.getStackSize() == 0:
                return
            self.__displayMenu()
            op = self.__readOption()
            if Menu.getCurrentMenu().isOption(op):
                self.getNextOption(op)
            else:
                print("Optiunea aleasa trebuie sa fie din multimea " +
                      str(list(Menu.getCurrentMenu().getMenuFunctions().keys())) + "\n")

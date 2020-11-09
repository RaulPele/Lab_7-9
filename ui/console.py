from ui.menu import Menu
from validation.errors import InvalidStudentError, StudentAlreadyExistsError
from validation.errors import InvalidDisciplineError, DisciplineAlreadyExistsError
from utils.colors import  Colors

class Console:
    def __init__(self, studentSrv, disciplineSrv):
        self.__createMenu()
        self.__studentSrv = studentSrv
        self.__disciplineSrv = disciplineSrv

    def __createMenu(self):
        """
        Functia creaza meniul pentru utilizator
        """
        addStudentMenu = Menu()
        addStudentMenu.addItem("1. Adauga un student in facultate")
        addStudentMenu.addFunction(self.addStudent)
        addStudentMenu.addItem("2. Inapoi...")

        addDisciplineMenu = Menu()
        addDisciplineMenu.addItem("1. Adauga o disciplina la facultate")
        addDisciplineMenu.addFunction(self.addDiscipline)
        addDisciplineMenu.addItem("2. Inapoi...")

        mainMenu = Menu()
        mainMenu.addItem("1. Adauga student")
        mainMenu.addItem("2. Adauga disciplina")
        mainMenu.addItem("3. Iesire")
        mainMenu.addSubMenu(addStudentMenu)
        mainMenu.addSubMenu(addDisciplineMenu)
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

    def addDiscipline(self):
        name = input("Dati numele disciplinei: \n").strip()
        teacherFirst = input("Dati prenumele profesorului disciplinei: \n").strip()
        teacherLast = input("Dati numele profesorului disciplinei: \n").strip()
        isOptional = input("Este disciplina optionala? (Da, Nu) \n").strip()
        IDDiscipline = input("Dati ID-ul disciplinei: \n").strip()

        try:
            self.__disciplineSrv.addDiscipline(IDDiscipline, name, teacherFirst,teacherLast, isOptional)
        except InvalidDisciplineError as err:
            print(str(err))
        except DisciplineAlreadyExistsError as err:
            print(str(err))
        else:
            self.printDisciplines()
        input("Apasati enter pentru a continua...\n")

    def printStudents(self):
        """
        Afiseaza studentii din cadrul facultatii
        """
        students = self.__studentSrv.getStudents()
        print(Colors.RED + "Studentii din cadrul facultatii: \n")
        for student in students:
            print(Colors.RED + "ID: " + Colors.GREEN + student.getID())
            print(Colors.RED + "Nume: " + Colors.GREEN+ student.getLastName())
            print(Colors.RED + "Prenume: " + Colors.GREEN + student.getFirstName())
            print(Colors.RESET)

    def printDisciplines(self):
        disciplines = self.__disciplineSrv.getDisciplines()
        print (Colors.RED + "Disciplinele din cadrul facultatii: \n")
        for discipline in disciplines:
            print(discipline)

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

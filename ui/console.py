from ui.menu import Menu
from validation.errors import InvalidStudentError, StudentAlreadyExistsError, InvalidIDError
from validation.errors import InvalidDisciplineError, DisciplineAlreadyExistsError, NonExistentIDError
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
        addMenu = Menu()
        addMenu.addItem("1. Adauga un student in facultate")
        addMenu.addFunction(self.addStudent)
        addMenu.addItem("2. Adauga o disciplina la facultate")
        addMenu.addFunction(self.addDiscipline)
        addMenu.addItem("3. Inapoi...")


        printMenu = Menu()
        printMenu.addItem("1. Tipareste lista studentilor din facultate")
        printMenu.addFunction(self.printStudents)
        printMenu.addItem("2. Tipareste lista disciplinelor din facultate")
        printMenu.addFunction(self.printDisciplines)
        printMenu.addItem("3. Inapoi...")

        removeMenu = Menu()
        removeMenu.addItem("1. Sterge un student din lista")
        removeMenu.addFunction(self.removeStudent)
        removeMenu.addItem("2. Sterge o disciplina din lista")
        removeMenu.addFunction(self.removeDiscipline)
        removeMenu.addItem("3. Inapoi...")

        searchMenu = Menu()
        searchMenu.addItem("1. Afiseaza informatii despre un student din lista ")
        searchMenu.addFunction(self.findStudent)
        searchMenu.addItem("2. Inapoi...")


        mainMenu = Menu()
        mainMenu.addItem("1. Adaugare")
        mainMenu.addItem("2. Afisare")
        mainMenu.addItem("3. Stergere")
        mainMenu.addItem("4. Cautare")
        mainMenu.addItem("5. Iesire")
        mainMenu.addSubMenu(addMenu)
        mainMenu.addSubMenu(printMenu)
        mainMenu.addSubMenu(removeMenu)
        mainMenu.addSubMenu(searchMenu)
        Menu.initializeStack(mainMenu)

    def __displayMenu(self):
        """
        Afiseaza meniul curent pentru utilizator
        """
        currentMenu = Menu.getCurrentMenu()
        currentMenu.printMenu()

    def __readOption(self):
        """
        Citeste o optiune de la utilizator
        :return op: optiunea citita - string
        """
        op = input("Alege o optiune: \n")
        return op


    def getNextOption(self, op):
        """
        Executa urmatoarea actiune in functie de alegerea op a utilizatorului
        navigand prin meniu sau apeland functia corespunzatoare
        :param op: optiunea utilizatorului - string
        """
        if Menu.userExits(op):
            Menu.navigateBackwards()
            return
        currentMenu = Menu.getCurrentMenu()

        if op in currentMenu.getSubMenus().keys():
            Menu.navigateToSubmenu(op)
            return

        function = currentMenu.getFunction(op)
        function()

    def selectOptionals(self, student):
        """
        Preia de la utilizator datele corespunzatoare optionalelor si le adauga in lista de discipline
        pentru studentul student
        :param student: student tip Student()
        """
        disciplines = self.__disciplineSrv.getOptionals()
        if len(disciplines) == 0:
            return
        for discipline in disciplines:
            print(discipline)

        answer = input("Doriti sa alegeti discipline optionale? (Da, Nu)\n").lower()
        while answer not in ["da", "nu"]:
            answer = input("Doriti sa alegeti discipline optionale? (Da, Nu)\n").lower()

        if answer == "nu":
            return

        while len(disciplines) !=0:
            option = input("Dati id-ul disciplinei optionale dorite sau tastati exit: \n").lower()
            if option =="exit":
                break
            for i in range(0, len(disciplines)):
                if disciplines[i].getID() == option:
                    student.addDiscipline(disciplines[i])
                    del disciplines[i]
                    for discipline in disciplines:
                        print(discipline)

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
            self.selectOptionals(self.__studentSrv.findStudent(IDStudent))
            self.printStudents()
        input("Apasati Enter pentru a continua...\n")

    def addDiscipline(self):
        """
        Ia datele de la utilizator pentru adaugarea disciplinei si le transmite la serviciul corespunzator
        """
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

    def printStudents(self, message = "Studentii din cadrul facultatii: \n"):
        """
        Afiseaza studentii din cadrul facultatii
        """
        students = self.__studentSrv.getStudents()

        if len(students) == 0:
            print(Colors.GREEN+ "Lista studentilor este goala.\n" +Colors.RESET)
            return

        print(Colors.RED + message)
        for student in students:
            print(Colors.RED + "ID: " + Colors.GREEN + student.getID())
            print(Colors.RED + "Nume: " + Colors.GREEN+ student.getLastName())
            print(Colors.RED + "Prenume: " + Colors.GREEN + student.getFirstName())
            print(Colors.RESET)

    def printDisciplines(self, message = "Disciplinele din cadrul facultatii: \n"):
        "Afiseaza lista de discipline din cadrul facultatii"
        disciplines = self.__disciplineSrv.getDisciplines()

        if len(disciplines) == 0:
            print(Colors.GREEN + "Lista disciplinelor este goala.\n" + Colors.RESET)
            return

        print (Colors.RED + message)
        for discipline in disciplines:
            print(discipline)

    def removeStudent(self):
        """
        Ia datele de la utilizator pentru stergerea studentului si apeleaza serviciul corespunzator
        """
        if len(self.__studentSrv.getStudents()) == 0:
            print(Colors.GREEN + "Lista este goala.\n" + Colors.RESET)
            return
        self.printStudents()

        identifier = input("Dati ID-ul studentului care se va elimina: ")
        try:
            self.__studentSrv.removeStudent(identifier)
        except InvalidIDError as err:
            print(str(err))
        except NonExistentIDError as err:
            print(str(err))
        else:
            self.printStudents("Lista de studenti obtinuta in urma eliminarii: \n")
            input("Apasati Enter pentru a continua...")

    def removeDiscipline(self):
        "Ia datele de la utilizator pentru stergerea unei discipline si apeleaza serviciul corespunzator"
        if len(self.__disciplineSrv.getDisciplines()) == 0:
            print(Colors.GREEN + "Lista este goala.\n" + Colors.RESET)
            return
        self.printDisciplines()

        identifier = input("Dati ID-ul disciplinei care se va elimina: ")
        try:
            self.__disciplineSrv.removeDiscipline(identifier)
        except InvalidIDError as err:
            print(str(err))
        except NonExistentIDError as err:
            print(str(err))
        else:
            self.printDisciplines("Lista de discipline obtinuta in urma eliminarii: \n")
            input("Apasa Enter pentru a continua...")

    def findStudent(self):
        """Ia datele de la utilizator pentru afisarea datelor despre un student
        si apeleaza serviciul corespunzator"""
        if len(self.__studentSrv.getStudents()) == 0:
            print(Colors.GREEN + "Lista este goala.\n" + Colors.RESET)
            return
        self.printStudents()

        identifier = input("Dati ID-ul studentului pentru care se va face afisarea: \n")
        try:
            student = self.__studentSrv.findStudent(identifier)
        except InvalidIDError as err:
            print(str(err))
        except NonExistentIDError as err:
            print(str(err))
        else:
            print(student)

    def run(self):
        """Functia principala care executa programul"""
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

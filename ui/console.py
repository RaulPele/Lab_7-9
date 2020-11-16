from ui.menu import Menu
from validation.errors import InvalidStudentError, StudentAlreadyExistsError, InvalidIDError
from validation.errors import InvalidDisciplineError, DisciplineAlreadyExistsError, NonExistentIDError
from validation.errors import InvalidGradeError, NonExistentStudentError, NonExistentDisciplineError
from validation.errors import InvalidNameError
from utils.colors import  Colors

class Console:
    def __init__(self, studentSrv, disciplineSrv, gradeSrv):
        self.__createMenu()
        self.__studentSrv = studentSrv
        self.__disciplineSrv = disciplineSrv
        self.__gradeSrv = gradeSrv

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

        gradesMenu = Menu()
        gradesMenu.addItem("1. Asigneaza o nota unui student la o materie")
        gradesMenu.addFunction(self.assignGrade)
        gradesMenu.addItem("2. Inapoi...")

        modifyMenu = Menu()
        modifyMenu.addItem("1. Modifica un student din lista")
        modifyMenu.addFunction(self.modifyStudent)
        modifyMenu.addItem("2. Modifica o disciplina din lista")
        modifyMenu.addFunction(self.modifyDiscipline)
        modifyMenu.addItem("3. Inapoi...")


        mainMenu = Menu()
        mainMenu.addItem("1. Adaugare")
        mainMenu.addItem("2. Afisare")
        mainMenu.addItem("3. Stergere")
        mainMenu.addItem("4. Modificare")
        mainMenu.addItem("5. Cautare")
        mainMenu.addItem("6. Note")
        mainMenu.addItem("7. Iesire")
        mainMenu.addSubMenu(addMenu)
        mainMenu.addSubMenu(printMenu)
        mainMenu.addSubMenu(removeMenu)
        mainMenu.addSubMenu(modifyMenu)
        mainMenu.addSubMenu(searchMenu)
        mainMenu.addSubMenu(gradesMenu)
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

    def selectOptionals(self, IDStudent):
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
            for discipline in disciplines:
                print(discipline)

            option = input("Dati id-ul disciplinei optionale dorite sau tastati exit: \n").lower()
            if option =="exit":
                break
            try:
                self.__disciplineSrv.selectOptionals(IDStudent, option)
            except InvalidIDError as err:
                print(str(err))
            except NonExistentIDError as err:
                print(str(err))
            else:
                disciplines = [d for d in disciplines if d.getID()!=option]

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
            self.selectOptionals(IDStudent)
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

        identifier = input("Dati ID-ul sau numele (prenume nume) studentului care se va elimina: ").strip()
        try:
            self.__studentSrv.removeStudent(identifier)
        except NonExistentStudentError as err:
            print(str(err))
        except InvalidStudentError as err:
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

        identifier = input("Dati ID-ul sau numele disciplinei care se va elimina: ")

        try:
            self.__disciplineSrv.removeDiscipline(identifier)
        except InvalidDisciplineError as err:
            print(str(err))
        except NonExistentDisciplineError as err:
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

        identifier = input("Dati ID-ul sau numele studentului pentru care se va face afisarea: \n")
        try:
            student = self.__studentSrv.findStudent(identifier)
        except InvalidStudentError as err:
            print(str(err))
        except NonExistentStudentError as err:
            print(str(err))
        else:
            if isinstance(student, list):
                for st in student:
                    print(st)
            else:
                print(student)

            input("Apsati Enter pentru a continua...")

    def __modifyStudentID(self, IDStudent):
        newID = input("Dati ID-ul nou al studentului: ").strip()

        try:
            self.__studentSrv.modifyID(IDStudent, newID)
        except InvalidIDError as err:
            print(str(err))

    def __modifyStudentName(self, IDStudent):
        firstName = input("Dati prenumele nou al studentului:\n").strip()
        lastName = input("Dati numele nou al studentului:\n").strip()
        try:
            self.__studentSrv.modifyName(IDStudent, firstName, lastName)
        except InvalidNameError as err:
            print(str(err))

    def __modifyStudentOptionals(self, IDStudent):
        operation = input("Doriti sa adaugati(1) sau sa stergeti(2) discipline optionale?\n")
        functions = {"1": self.__addOptionals, "2": self.__removeOptionals}
        try:
            functions[operation](IDStudent)
        except KeyError:
            print("Optiune invalida!\n")

    def __addOptionals(self, IDStudent):
        optionals = self.__disciplineSrv.getOptionals()
        studentOptionals = self.__studentSrv.getOptionals(IDStudent)
        availableOptionals = [d for d in optionals if d not in studentOptionals]

        if len(availableOptionals) == 0:
            print(Colors.RED + "Nu exista alte optionale disponibile.\n" + Colors.RESET)
            return

        while len(availableOptionals) != 0:
            for d in availableOptionals:
                print(d)

            prompt = input("Dati id-ul disciplinei optionale sau tastati exit: \n").strip()
            if prompt == "exit":
                return
            try:
                self.__disciplineSrv.selectOptionals(IDStudent, prompt)
            except InvalidIDError as err:
                print(str(err))
            except NonExistentIDError as err:
                print(str(err))
            else:
                availableOptionals = [d for d in availableOptionals if d.getID() != prompt]

    def __removeOptionals(self, IDStudent):
        studentOptionals = self.__studentSrv.getOptionals(IDStudent)

        if len(studentOptionals) == 0 :
            print(Colors.RED + "Studentul nu are selectate optionale.\n" + Colors.RESET)
            return

        while len(studentOptionals) != 0:
            for d in studentOptionals:
                print(d)

            prompt = input("Dati id-ul disciplinei optionale sau tastati exit: \n").strip()
            if prompt == "exit":
                return
            try:
                self.__disciplineSrv.removeOptionals(IDStudent, prompt)
            except InvalidIDError as err:
                print(str(err))
            except NonExistentIDError as err:
                print(str(err))
            else:
                studentOptionals = [d for d in studentOptionals if d.getID() != prompt]

    def modifyStudent(self):
        """
        Ia datele necesare pentru modificarea unui student si apeleaza serviciul corespunzator
        """
        if len(self.__studentSrv.getStudents()) == 0:
            print(Colors.GREEN + "Lista este goala.\n" + Colors.RESET)
            return

        self.printStudents()

        IDStudent = input("Dati ID-ul studentului care se va modifica:\n").strip()

        try:
            self.__studentSrv.findStudent(IDStudent)
        except InvalidIDError as err:
            print(str(err))
            return
        except NonExistentIDError as err:
            print(str(err))
            return

        property = input("Selectati campul care se va modifica (ID, nume, discipline): \n").strip().lower()
        modFunctions = {"id": self.__modifyStudentID, "nume": self.__modifyStudentName, "discipline": self.__modifyStudentOptionals}

        try:
            modFunctions[property](IDStudent)
        except KeyError:
            print(Colors.RED + "Campul selectat nu exista!\n" + Colors.RESET)
        else:
            print(Colors.GREEN + "Studentul a fost modificat cu succes!\n" + Colors.RESET)
            input("Apasati enter pentru a continua...\n")

    def modifyDiscID(self, IDDiscipline):
        newID = input("Introduceti noul id al disciplinei: ").strip()
        try:
            self.__disciplineSrv.modifyID(IDDiscipline, newID)
        except InvalidIDError as err:
            print(str(err))
        except NonExistentIDError as err:
            print(str(err))


    def modifyDiscName(self, IDDiscipline):
        newName = input("Introduceti noul nume al disciplinei: ").strip()
        try:
            self.__disciplineSrv.modifyDiscName(IDDiscipline, newName)
        except InvalidNameError as err:
            print(str(err))

    def modifyDiscTeacher(self, IDDiscipline):
        newFirstName = input("Introduceti noul prenume al profesorului: ").strip()
        newLastName = input("Introduceti noul nume al profesorului: ").strip()

        try:
            self.__disciplineSrv.modifyTeacher(IDDiscipline, newFirstName, newLastName)
        except InvalidNameError as err:
            print(str(err))

    def modifyDiscOptional(self, IDDiscipline):
        newOptional = input("Este disciplina optionala? (Da/Nu)").strip().lower()
        options = {"da":True, "nu": False}
        if newOptional not in options.keys():
            print(Colors.RED + "Optiune invalida!\n" + Colors.RESET)
            return
        self.__disciplineSrv.modifyOptional(IDDiscipline, options[newOptional])

    def modifyDiscipline(self):
        """
        Ia datele necesare pentru a modifica o disciplina si apeleaza serviciul corespunzator
        """
        if len(self.__disciplineSrv.getDisciplines()) == 0:
            print(Colors.GREEN + "Lista este goala.\n" + Colors.RESET)
            return
        self.printDisciplines()

        IDDiscipline = input("Dati id-ul disciplinei care se va modifica: ").strip()
        try:
            self.__disciplineSrv.findDiscipline(IDDiscipline)
        except InvalidIDError as err:
            print(str(err))
            return
        except NonExistentIDError as err:
            print(str(err))
            return

        property = input("Selectati campul care se va modifica (ID, nume, profesor, optional): \n").strip().lower()
        modFunctions = {"id": self.modifyDiscID, "nume": self.modifyDiscName, "profesor": self.modifyDiscTeacher,
                        "optional": self.modifyDiscOptional}

        try:
            modFunctions[property](IDDiscipline)

        except KeyError:
            print(Colors.RED + "Campul selectat nu exista!\n" + Colors.RESET)
        else:
            print(Colors.GREEN + "Disciplina a fost modificata cu succes!\n" + Colors.RESET)
            input("Apasati enter pentru a continua...")


    def assignGrade(self):
        """
        Ia datele necesare pentru a atribui o nota unui student la o materie
        raise InvalidIDError - daca id-ul studentului sau al disciplinei nu este corect
        """
        if len(self.__studentSrv.getStudents())==0:
            print(Colors.GREEN + "Lista studentilor este goala.\n" + Colors.RESET)
            return
        if len(self.__disciplineSrv.getDisciplines())==0:
            print(Colors.GREEN + "Lista disciplinelor este goala.\n" + Colors.RESET)
            return
        self.printStudents()

        identifier = input("Dati ID-ul studentului care primeste nota: \n")
        try:
            student = self.__studentSrv.findStudent(identifier)
        except InvalidIDError as err:
            print(str(err))
        except NonExistentIDError as err:
            print(str(err))
        else:
            print(student)
            disciplineIdentifier = input("Dati ID-ul disciplinei la care va primi studentul nota: \n")
            grade = input("Dati nota: \n")
            try:
                grade = float(grade)
            except ValueError:
                print("Nota trebuie sa fie de tipul float!\n")
                return

            try:
                self.__gradeSrv.assignGrade(identifier, disciplineIdentifier, grade)
            except InvalidIDError as err:
                print(str(err))
            except InvalidGradeError as err:
                print(str(err))
            except NonExistentIDError as err:
                print(str(err))
            else:
                print(student)
                input("Apasati Enter pentru a continua...")


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

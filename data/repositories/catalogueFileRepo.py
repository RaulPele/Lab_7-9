from data.repositories.catalogue import Catalogue
from domain.student import Student
from domain.discipline import Discipline
from validation.errors import StudentAlreadyExistsError, NonExistentStudentError, NonExistentIDError

class CatalogueFileRepository(Catalogue):

    def __init__(self, studentFileName, disciplineFileName, optionalsFileName="optionals.txt"):
        super().__init__()
        self.__studentFileName = studentFileName
        self.__disciplineFileName = disciplineFileName
        self.__optionalFileName = optionalsFileName

        self.__loadDisciplinesFromFile()
        self.__loadStudentsFromFile()

    def __getStudentOptionals(self, studentID):
        """
        Returneaza disciplinele optionale selectate de studentul studentID
        :param studentID: string
        :return optionals: lista de obiecte reprezentand optionalele studentului
        """
        optionals = []
        try:
            optFile = open(self.__optionalFileName, "r")
        except IOError:
            return optionals

        for line in optFile:
            attr = line.strip().split(",")
            if attr[0] == studentID:
                for i in range (1, len(attr)):
                    discipline = self.findDisciplineByID(attr[i])
                    optionals.append(discipline)
                break #am gasit deja studentul -> iesim

        optFile.close()
        return optionals



    def __readStudentFromFile(self, line):
        """
        Citeste un student dintr-un fisier si returneaza obiectul
        :param line: linia de pe care se citeste studentul - string
        :return student: obiectul corespunzator studentului
        """
        #structura unei linii din fisier: IDStudent,Prenume,Nume
        attr = line.split(",")
        student = Student(attr[0], attr[1], attr[2])

        optionals = self.__getStudentOptionals(attr[0])
        if len(optionals) !=0:
            for opt in optionals:
                student.addDiscipline(opt)

        return student


    def __readDisciplineFromFile(self, line):
        """
        Citeste o disciplina dintr-un fisier si returneaza obiectul
        :param line: linia de pe care se citeste disciplina - string
        :return discipline: Discipline()
        """
        # structura unei linii din fisier: IDDiscipline,name,teacherFirst,teacherLast,isOptional
        attr = line.split(",")
        if attr[4] == "True":
            isOptional = True
        else:
            isOptional = False

        discipline = Discipline(attr[0], attr[1], attr[2], attr[3], isOptional)
        return discipline


    def __loadStudentsFromFile(self):
        """
        Initializeaza lista de studenti din superclass cu datele din fisier
        """
        super().clearStudentsList()
        try:
            studFile = open(self.__studentFileName, "r")
        except IOError:
            return

        for line in studFile:
            line = line.strip()
            if line == "":
                continue
            student = self.__readStudentFromFile(line)
            try:
                super().addStudent(student)
            except StudentAlreadyExistsError as err:
                #print(str(err)) #TODO: remove line from file
                pass

        studFile.close()


    def __loadDisciplinesFromFile(self):
        """
        Initializeaza lista de discipline din superclass cu datele din fisier
        """
        try:
            discFile = open(self.__disciplineFileName, "r")
        except IOError:
            return

        for line in discFile:
            line = line.strip()
            if line == "":
                continue

            discipline = self.__readDisciplineFromFile(line)
            super().addDiscipline(discipline)

        discFile.close()

    def __appendStudent(self, student):
        """
        Adauga un student la fisierul de studenti
        :param student: studentul care va fi adaugat
        """
        studentStr = student.getID() + "," + student.getFirstName() +"," + student.getLastName()

        studentStr += '\n'
        with open(self.__studentFileName, "a") as studFile:
            studFile.write(studentStr)


    def __appendDiscipline(self, discipline):
        """
        Adauga o disciplina la fisierul de discipline
        """

        discStr = discipline.getID()+"," + discipline.getName() +"," + discipline.getTeacherFirst() +","\
                +discipline.getTeacherLast() + "," + str(discipline.getIsOptional()) +"\n"

        with open(self.__disciplineFileName, "a") as discFile:
            discFile.write(discStr)

    def __storeAllStudents(self):
        """
        Suprascrie fisierul de studenti cu  toti studentii din lista de studenti din superclass
        """
        with open(self.__studentFileName, "w") as studFile:
            for student in super().getStudents():
                studentStr = student.getID() + "," + student.getFirstName() + "," + student.getLastName()
                studentStr += "\n"
                studFile.write(studentStr)

    def __storeAllDisciplines(self):
        """
        Suprascrie fisierul de discipline cu toate disciplinele din lista de discipline din superclass
        """

        with open(self.__disciplineFileName, "w") as discFile:
            for discipline in self.getDisciplines():
                discStr = discipline.getID() + "," + discipline.getName() + "," + discipline.getTeacherFirst() + "," \
                          + discipline.getTeacherLast() + "," + str(discipline.getIsOptional()) + "\n"
                discFile.write(discStr)

    def __storeAllOptionals(self):
        """
        Suprascrie fisierul cu  disciplinele optionale corespunzatoare fiecarui student
        """

        with open(self.__optionalFileName, "w") as optFile:
            for student in self.getStudents():
                optStr = student.getID()

                optionals = student.getOptionals()
                if len(optionals) == 0:
                    continue
                for opt in optionals:
                    optStr += "," + opt.getID()
                optStr += "\n"
                optFile.write(optStr)

    def selectOptionalsByID(self, IDStudent, IDDiscipline):
        """
        Adauga disciplina optionala IDDiscipline la lista de discipline a studentului IDStudent
        :param IDStudent: id-ul studentului - string
        :param IDDiscipline: id-ul disciplinei - string
        """

        super().selectOptionalsByID(IDStudent, IDDiscipline)
        self.__storeAllOptionals()

    def removeOptionalsByID(self, IDStudent, IDDiscipline):
        """
        Sterge disciplina optionala IDDiscipline din lista de discipline a studentului IDStudent
        :param IDStudent: id-ul studentului - string
        :param IDDiscipline: id-ul disciplinei - string
        """

        super().removeOptionalsByID(IDStudent, IDDiscipline)
        self.__storeAllOptionals()

    def addStudent(self, newStudent):
        """
        Adauga un student in fisierul de studenti
        :param newStudent: studentul care se adauga
        """
        self.__checkUpdateStudentsFile()
        super().addStudent(newStudent)
        self.__appendStudent(newStudent)

    def addDiscipline(self, newDiscipline):
        """
        Adauga o disciplina in fisierul de discipline
        :param newDiscipline: disciplina care se adauga
        """

        super().addDiscipline(newDiscipline)
        self.__appendDiscipline(newDiscipline)

    def removeStudentByID(self, ID):
        """
        Sterge studentul cu id-ul ID din fisierul de studenti
        :param ID: id-ul studentului care se va sterge - string
        """
        #print(len(super().getStudents()))
        self.__checkUpdateStudentsFile()
        #print(len(super().getStudents()))

        try:
            super().removeStudentByID(ID)
        except NonExistentIDError as err:
            print (str(err))
            return
        self.__storeAllStudents()
        self.__storeAllOptionals() # todo: only rewrite optionals if student had optionals

    def removeStudentByName(self, name):
        """
        Sterge studentii cu numele name din fisierul de studenti
        :param name: numele studentilor - string
        """

        self.__checkUpdateStudentsFile()
        try:
            super().removeStudentByName(name)
        except NonExistentStudentError as err:
            print(str(err))
            return
        self.__storeAllStudents()
        self.__storeAllOptionals() # todo: only rewrite optionals if student had optionals


    def removeDisciplineByID(self, ID):
        """
        Sterge disciplina cu id-ul ID din fisierul de discipline
        :param ID: id-ul disciplinei care se va sterge - string
        """

        super().removeDisciplineByID(ID)
        self.__storeAllDisciplines()
        self.__storeAllOptionals() #todo: only rewrite optionals if discipline is optional


    def removeDisciplineByName(self, name):
        """
        Sterge disciplinele cu numele name din fisierul de discipline
        :param name: numele disciplinelor care se vor sterge - string
        """

        super().removeDisciplineByName(name)
        self.__storeAllDisciplines()
        self.__storeAllOptionals() # todo: only rewrite optionals if discipline is optionals

    def modifyDiscID(self, discipline, newID):
        """
        Modifica id-ul disciplinei discipline
        :param discipline: obiect Discipline()
        :param newID: id-ul nou - string
        """

        super().modifyDiscID(discipline, newID)
        self.__storeAllDisciplines()

        if discipline.getIsOptional():
            self.__storeAllOptionals()

    def modifyDiscName(self, discipline, newName):
        """
        Modifica numele disciplinei discipline
        :param discipline: obiect Discipline()
        :param newName: numele nou - string
        """

        super().modifyDiscName(discipline, newName)
        self.__storeAllDisciplines()

    def modifyDiscOptional(self, discipline, isOptional):
        """
        Modifica caracterul optional al unei discipline
        :param discipline: obiect Discipline()
        :param isOptional: noul caracter al disciplinei - optional sau obligatoriu - True sau False
        """

        old = discipline.getIsOptional()
        super().modifyDiscOptional(discipline, isOptional)
        if old != isOptional:
            self.__storeAllDisciplines()
            self.__storeAllOptionals()

    def modifyDiscTeacher(self, discipline, newFirstName, newLastName):
        """
        Modifica numele profesorului unei discipline
        :param discipline: obiect Discipline()
        :param newFirstName: noul prenume al profesorului - string
        :param newLastName: noul nume al profesorului - string
        """

        super().modifyDiscTeacher(discipline ,newFirstName, newLastName)
        self.__storeAllDisciplines()

    def modifyStudentID(self, student, newID):
        """Modifica id-ul unui student
        :param student: obiect Student()
        :param newID: noul id al studentului - string"""

        self.__checkUpdateStudentsFile()
        super().modifyStudentID(student, newID)
        self.__storeAllStudents()

        if len(student.getOptionals()) != 0:
            self.__storeAllOptionals()

    def modifyStudentName(self, student, newFirstName, newLastName):
        """
        Modifica numele studentului
        :param student: obiect Student()
        :param newFirstName: nou prenume -string
        :param newLastName: noul nume - string
        """
        self.__checkUpdateStudentsFile()
        super().modifyStudentName(student, newFirstName, newLastName)
        self.__storeAllStudents()

    def __checkUpdateStudentsFile(self):
        self.__loadStudentsFromFile()

    def getStudents(self):
        self.__checkUpdateStudentsFile()
        return super().getStudents()

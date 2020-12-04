from data.repositories.catalogue import Catalogue
from domain.student import Student
from domain.discipline import Discipline

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
        try:
            studFile = open(self.__studentFileName, "r")
        except IOError:
            return

        for line in studFile:
            line = line.strip()
            if line == "":
                continue
            student = self.__readStudentFromFile(line)
            super().addStudent(student)

        studFile.close()


    def __loadDisciplinesFromFile(self):
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

        studentStr = student.getID() + "," + student.getFirstName() +"," + student.getLastName()

        studentStr += '\n'
        with open(self.__studentFileName, "a") as studFile:
            studFile.write(studentStr)


    def __appendDiscipline(self, discipline):
        discStr = discipline.getID()+"," + discipline.getName() +"," + discipline.getTeacherFirst() +","\
                +discipline.getTeacherLast() + "," + str(discipline.getIsOptional()) +"\n"

        with open(self.__disciplineFileName, "a") as discFile:
            discFile.write(discStr)

    def __storeAllStudents(self):
        with open(self.__studentFileName, "w") as studFile:
            for student in self.getStudents():
                studentStr = student.getID() + "," + student.getFirstName() + "," + student.getLastName()
                studentStr += "\n"
                studFile.write(studentStr)

    def __storeAllDisciplines(self):
        with open(self.__disciplineFileName, "w") as discFile:
            for discipline in self.getDisciplines():
                discStr = discipline.getID() + "," + discipline.getName() + "," + discipline.getTeacherFirst() + "," \
                          + discipline.getTeacherLast() + "," + str(discipline.getIsOptional()) + "\n"
                discFile.write(discStr)

    def __storeAllOptionals(self):
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
        super().selectOptionalsByID(IDStudent, IDDiscipline)
        self.__storeAllOptionals()

    def removeOptionalsByID(self, IDStudent, IDDiscipline):
        super().removeOptionalsByID(IDStudent, IDDiscipline)
        self.__storeAllOptionals()

    def addStudent(self, newStudent):
        super().addStudent(newStudent)
        self.__appendStudent(newStudent)

    def addDiscipline(self, newDiscipline):
        super().addDiscipline(newDiscipline)
        self.__appendDiscipline(newDiscipline)

    def removeStudentByID(self, ID):
        super().removeStudentByID(ID)
        self.__storeAllStudents()
        self.__storeAllOptionals() # todo: only rewrite optionals if student had optionals

    def removeStudentByName(self, name):
        super().removeStudentByName(name)
        self.__storeAllStudents()
        self.__storeAllOptionals() # todo: only rewrite optionals if student had optionals


    def removeDisciplineByID(self, ID):
        super().removeDisciplineByID(ID)
        self.__storeAllDisciplines()
        self.__storeAllOptionals() #todo: only rewrite optionals if discipline is optional


    def removeDisciplineByName(self, name):
        super().removeDisciplineByName(name)
        self.__storeAllDisciplines()
        self.__storeAllOptionals() # todo: only rewrite optionals if discipline is optionals

    def modifyDiscID(self, discipline, newID):
        super().modifyDiscID(discipline, newID)
        self.__storeAllDisciplines()

        if discipline.getIsOptional():
            self.__storeAllOptionals()

    def modifyDiscName(self, discipline, newName):
        super().modifyDiscName(discipline, newName)
        self.__storeAllDisciplines()

    def modifyDiscOptional(self, discipline, isOptional):
        old = discipline.getIsOptional()
        super().modifyDiscOptional(discipline, isOptional)
        if old != isOptional:
            self.__storeAllDisciplines()
            self.__storeAllOptionals()

    def modifyDiscTeacher(self, discipline, newFirstName, newLastName):
        super().modifyDiscTeacher(discipline ,newFirstName, newLastName)
        self.__storeAllDisciplines()

    def modifyStudentID(self, student, newID):
        super().modifyStudentID(student, newID)
        self.__storeAllStudents()

        if len(student.getOptionals()) != 0:
            self.__storeAllOptionals()

    def modifyStudentName(self, student, newFirstName, newLastName):
        super().modifyStudentName(student, newFirstName, newLastName)
        self.__storeAllStudents()
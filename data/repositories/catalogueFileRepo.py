from data.repositories.catalogue import Catalogue
from domain.student import Student
from domain.discipline import Discipline

class CatalogueFileRepository(Catalogue):

    def __init__(self, studentFileName, disciplineFileName):
        super().__init__()
        self.__studentFileName = studentFileName
        self.__disciplineFileName = disciplineFileName

        self.__loadDisciplinesFromFile()
        self.__loadStudentsFromFile()

    def __readStudentFromFile(self, line):
        """
        Citeste un student dintr-un fisier si returneaza obiectul
        :param line: linia de pe care se citeste studentul - string
        :return student: obiectul corespunzator studentului
        """
        #structura unei linii din fisier: IDStudent,Prenume,Nume\n
        attr = line.split(",")
        student = Student(attr[0], attr[1], attr[2])
        return student


    def __readDisciplineFromFile(self, line):
        """
        Citeste o disciplina dintr-un fisier si returneaza obiectul
        :param line: linia de pe care se citeste disciplina - string
        :return discipline: Discipline()
        """
        #structura unei linii din fisier: IDDiscipline,name,teacherFirst,teacherLast,isOptional
        attr = line.split(",")
        discipline = Discipline(attr[0], attr[1], attr[2], attr[3], attr[4])
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
            #TODO: read student optionals
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
            super().addDiscipline(Discipline)

        discFile.close()


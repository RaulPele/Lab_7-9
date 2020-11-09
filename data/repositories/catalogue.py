
from validation.errors import  StudentAlreadyExistsError

class Catalogue():
    def __init__(self):
        self.__students = []
        self.__disciplines = []

    def __enrollStudent(self, newStudent):
        """
        Ii atribuie studentului newStudent disciplinele obligatorii din catalog
        :param newStudent: obiect Student
        """
        for discipline in self.__disciplines:
            if not discipline.isOptional:
                newStudent.addDiscipline(discipline)

    def addStudent(self, newStudent):
        """
        Adauga studentul newStudent pe pozitia corespunzatoare in lista de studenti
        in ordine alfabetica
        raise StudentAlreadyExistsError daca student se afla deja in lista
        :param newStudent: obiect Student
        """
        if len(self.__students) == 0:
            self.__students.append(newStudent)
            self.__enrollStudent(newStudent)
            return

        if newStudent in self.__students:
            raise StudentAlreadyExistsError("Studentul se afla deja in lista!\n")

        oldSize = len(self.__students)
        for i in range(0, oldSize):
            currentStudent = self.__students[i]
            if newStudent.getLastName() < currentStudent.getLastName() or\
                    (newStudent.getLastName() == currentStudent.getLastName() and
                    newStudent.getFirstName() < currentStudent.getFirstName()):
                self.__students.insert(i, newStudent)
                break

        if oldSize == len(self.__students):
            self.__students.append(newStudent)

        self.__enrollStudent(newStudent)

    def getStudents(self):
        return self.__students
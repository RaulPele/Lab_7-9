
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
        raise StudentAlreadyexistsError daca student se afla deja in lista
        :param newStudent: obiect Student
        """
        if newStudent in self.__students:
            raise StudentAlreadyExistsError("Studentul se afla deja in lista!")
        for i in range(0, len(self.__students)):
            currentStudent = self.__students[i]
            if newStudent.getLastName() > currentStudent.getLastName() or\
                    (newStudent.getLastName() == currentStudent.getLastName() and
                    newStudent.getFirstName() > currentStudent.getFirstName()):
                self.__students.insert(i+1, newStudent)
                break
        self.__enrollStudent(newStudent)



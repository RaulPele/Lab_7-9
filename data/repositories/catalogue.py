
from validation.errors import  StudentAlreadyExistsError, DisciplineAlreadyExistsError, NonExistentIDError

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
            if  discipline.getIsOptional() == False:
                newStudent.addDiscipline(discipline)

    def addStudent(self, newStudent):
        """
        Adauga studentul newStudent pe pozitia corespunzatoare in lista de studenti
        in ordine alfabetica
        raise StudentAlreadyExistsError daca student se afla deja in lista
        :param newStudent: obiect Student
        """
        oldSize = len(self.__students)
        if oldSize == 0:
            self.__students.append(newStudent)
            self.__enrollStudent(newStudent)
            return

        if newStudent in self.__students:
            raise StudentAlreadyExistsError("Studentul se afla deja in lista!\n")

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

    def addDisciplineToStudents(self, newDiscipline):
        for student in self.__students:
            student.addDiscipline(newDiscipline)

    def addDiscipline(self, newDiscipline):
        """
        Adauga disciplina newDiscipline pe pozitia corespunzatoare pentru a respecta
        ordonarea alfabetica a listei de discipline
        raise DisciplineAlreadyExists - daca disciplina exista deja in lista
        :param newDiscipline: obiect Discipline()
        """
        oldSize = len(self.__disciplines)
        if oldSize == 0:
            self.__disciplines.append(newDiscipline)
            if newDiscipline.getIsOptional() == False:
                self.addDisciplineToStudents(newDiscipline)
            return

        if newDiscipline in self.__disciplines:
            raise DisciplineAlreadyExistsError("Disciplina exista deja in facultate!\n")

        for i in range(0, oldSize):
            currentDiscipline = self.__disciplines[i]
            if currentDiscipline.getName() > newDiscipline.getName():
                self.__disciplines.insert(i, newDiscipline)
                break

        if oldSize == len(self.__disciplines):
            self.__disciplines.append(newDiscipline)

        if newDiscipline.getIsOptional() == False:
            self.addDisciplineToStudents(newDiscipline)
        return

    def removeStudentByID(self, ID):
        for i in range(0, len(self.__students)):
            student = self.__students[i]
            if student.getID() == ID:
                del self.__students[i]
                return
        raise NonExistentIDError("ID-ul dat nu se afla in lista studentilor!\n")

    def removeDisciplineForStudents(self, discipline):
        for student in self.getStudents():
            student.removeDiscipline(discipline)

    def removeDisciplineByID(self, ID):
        for i in range(0, len(self.__disciplines)):
            discipline = self.__disciplines[i]
            if discipline.getID() == ID:
                self.removeDisciplineForStudents(discipline)
                del self.__disciplines[i]
                return
        raise NonExistentIDError("Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n")

    def findStudentByID(self, ID):
        for student in self.__students:
            if student.getID() == ID:
                return student
        raise NonExistentIDError("Studentul cu ID-ul dat nu se afla in lista studentilor!\n")


    def getStudents(self):
        return self.__students

    def getDisciplines(self):
        return self.__disciplines
from domain.student import Student
from validation.errors import InvalidStudentError, StudentAlreadyExistsError, InvalidDisciplineError
from validation.errors import DisciplineAlreadyExistsError, InvalidIDError, NonExistentIDError
from validation.errors import InvalidGradeError

class StudentService:
    """
    Serviciu pentru adaugare student in lista
    """
    def __init__(self, catalogue, validator):
        self.__catalogue = catalogue
        self.__validator = validator

    def addStudent(self, IDStudent, firstName, lastName):
        """
        Creeaza un nou student, il valideaza si il adauga in catalog
        raise InvalidStudentError-  daca datele studentului nu sunt valide
        raise StudentAlreadyExistsError - daca studentul se afla deja in lsita
        :param IDStudent: string - id-ul studentului
        :param firstName: string - prenumele studentului
        :param lastName: string - numele studentului
        """
        newStudent = Student(IDStudent, firstName, lastName)
        try:
            self.__validator.validateStudent(newStudent)
        except InvalidStudentError as err:
            raise InvalidStudentError(str(err))

        try:
            self.__catalogue.addStudent(newStudent)
        except StudentAlreadyExistsError as err:
            raise StudentAlreadyExistsError(str(err))

    def getStudents(self):
        "returneaza lista studentilor din catalog"
        return self.__catalogue.getStudents()

    def removeStudent(self, identifier):
        """
        Sterge studentul identificat dupa identifier din catalog
        raise InvalidIDError - daca id-ul nu este valid
        raise NonExistentIDError - daca id-ul este valid dar nu se afla in lista studentilor
        :param identifier: identificator pentru student - string
        """
        try:
            self.__validator.validateID(identifier)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            self.__catalogue.removeStudentByID(identifier)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))

    def findStudent(self, identifier):
        """
        Returneaza studentul identificat dupa identifier
        :param identifier: string - identificator pentru student
        :return: student - studentul corespunzator lui identifier
        """
        try:
            self.__validator.validateID(identifier)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            student = self.__catalogue.findStudentByID(identifier)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))
        return student


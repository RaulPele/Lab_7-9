from data.student import Student
from data.discipline import  Discipline
from validation.errors import InvalidStudentError, StudentAlreadyExistsError

class StudentSrv:
    """
    Serviciu pentru adaugare student in lista
    """
    def __init__(self, catalogue, validator):
        self.__catalogue = catalogue
        self.__validator = validator

    def addStudent(self, IDStudent, firstName, lastName):
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
        return self.__catalogue.getStudents()

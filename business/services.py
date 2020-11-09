from domain.student import Student
from domain.discipline import  Discipline
from validation.errors import InvalidStudentError, StudentAlreadyExistsError, InvalidDisciplineError
from validation.errors import DisciplineAlreadyExistsError


class StudentSrv:
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
        return self.__catalogue.getStudents()


class DisciplineService:
    def __init__(self, catalogue, validator):
        self.__catalogue = catalogue
        self.__validator = validator

    def addDiscipline(self, IDDiscipline, name, teacherFirst, teacherLast, isOptional):
        """
        Creeaza o noua disciplina, o valideaza si o adauga in catalog
        raise InvalidDisciplineError: daca datele disciplinei sunt invalide
        raise DisciplineAlreadyExistsError: daca disciplina exista deja in lista
        :param IDDiscipline: string - id-ul disciplinei
        :param name: string - numele disciplinei
        :param teacher: string - profesorul disciplinei
        :param isOptional: boolean - caracterul disciplinei (optional sau obligatoriu)
        """
        newDiscipline = Discipline(IDDiscipline, name, teacherFirst, teacherLast, isOptional)
        try:
            self.__validator.validateDiscipline(newDiscipline)
        except InvalidDisciplineError as err:
            raise InvalidDisciplineError(str(err))

        try:
            self.__catalogue.addDiscipline(newDiscipline)
        except DisciplineAlreadyExistsError as err:
            raise DisciplineAlreadyExistsError(str(err))

    def getDisciplines(self):
        return self.__catalogue.getDisciplines()
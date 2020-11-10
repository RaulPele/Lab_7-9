from domain.student import Student
from domain.discipline import  Discipline
from validation.errors import InvalidStudentError, StudentAlreadyExistsError, InvalidDisciplineError
from validation.errors import DisciplineAlreadyExistsError, InvalidIDError, NonExistentIDError
from validation.errors import InvalidGradeError


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

    def assignGrade(self, studIdentifier, discIdentifier, grade):
        try:
            self.__validator.validateGrade(grade)
        except InvalidGradeError as err:
            raise InvalidGradeError(str(err))

        try:
            self.__catalogue.assignGrade(studIdentifier, discIdentifier, grade)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))





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

    def removeDiscipline(self, identifier):
        """
        Sterge disciplina identificata cu identifier din catalog
        :param identifier: identificator - string
        """
        try:
            self.__validator.validateID(identifier)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            self.__catalogue.removeDisciplineByID(identifier)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))


    def getDisciplines(self):
        "Returneaza lista de discipline din catalog"
        return self.__catalogue.getDisciplines()

    def getOptionals(self):
        "Returneaza lista de discipline optionale din catalog"
        return self.__catalogue.getOptionals()

    def selectOptionals(self, IDStudent, identifier):
        """Selecteaza disciplina optionala cu identificata prin identifier"""
        try:
            self.__validator.validateID(identifier)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            self.__catalogue.selectOptionalsByID(IDStudent, identifier)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))
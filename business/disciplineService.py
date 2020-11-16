
from domain.discipline import  Discipline
from validation.errors import  InvalidDisciplineError, NonExistentDisciplineError
from validation.errors import DisciplineAlreadyExistsError, InvalidIDError, NonExistentIDError, InvalidNameError


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
        except InvalidIDError:
            try:
                self.__validator.validateDisciplineName(identifier)
            except InvalidNameError:
                raise InvalidDisciplineError("Numele sau ID-ul disciplinei este invalid!\n")

            try:
                self.__catalogue.removeDisciplineByName(identifier)
            except NonExistentDisciplineError as err:
                raise NonExistentDisciplineError(str(err))
        else:
            try:
                self.__catalogue.removeDisciplineByID(identifier)
            except NonExistentDisciplineError as err:
                raise NonExistentDisciplineError(str(err))


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

    def removeOptionals(self, IDStudent, identifier):
        """
        Sterge disciplina optionala identificata cu identifier pentru studentul IDStudent
        :param IDStudent: id-ul studentului - string
        :param identifier: identificatorul disciplinei - string
        raise NonExistentIDError daca studentul sau disciplina cu id-ul dat nu exista
        raise InvalidIDError- daca id-ul disciplinei este invalid
        """
        try:
            self.__validator.validateID(identifier)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            self.__catalogue.removeOptionalsByID(IDStudent, identifier)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))
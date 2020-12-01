
from domain.discipline import  Discipline
from validation.errors import  InvalidDisciplineError, NonExistentDisciplineError
from validation.errors import DisciplineAlreadyExistsError, InvalidIDError, NonExistentIDError, InvalidNameError


class DisciplineService:
    def __init__(self, catalogue, gradeRepo, validator):
        self.__catalogue = catalogue
        self.__validator = validator
        self.__gradeRepo = gradeRepo

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
                disciplines = self.__catalogue.findDisciplineByName(identifier)
                self.__catalogue.removeDisciplineByName(identifier)

            except NonExistentDisciplineError as err:
                raise NonExistentDisciplineError(str(err))
            else:
                self.__removeDisciplineGradesByID([d.getID() for d in disciplines])
        else:
            try:
                self.__catalogue.removeDisciplineByID(identifier)
            except NonExistentIDError as err:
                raise NonExistentDisciplineError(str(err))
            else:
                self.__removeDisciplineGradesByID([identifier])

    def __removeDisciplineGradesByID(self, discIDs):
        for id in discIDs:
            try:
                self.__gradeRepo.removeDisciplineGradesByID(id)
            except NonExistentIDError:
                pass


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

    def findDiscipline(self, identifier):
        """Returneaza disciplina cu identificatorul identifier
         identifier - string
         return discipline - disciplina corespunzatoare Discipline()
        """
        try:
            self.__validator.validateID(identifier)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            discipline = self.__catalogue.findDisciplineByID(identifier)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))

        return discipline

    def modifyID(self, oldID, newID):
        """
        Modifica id-ul disciplinei din oldID in newID
        :param oldID: id-ul disciplinei - string
        :param newID: noul id al disciplinei - string
        raise InvalidIDError daca newID este invalid
        """
        try:
            self.__validator.validateID(newID)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            discipline = self.__catalogue.findDisciplineByID(oldID)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))

        self.__catalogue.modifyDiscID(discipline, newID)

    def modifyDiscName(self, IDDiscipline, newName):
        """
        Modifica numele disciplinei in newName
        :param IDDiscipline: id-ul disciplinei - string
        :param newName: noul nume al disciplinei - string
        raise InvalidNameError - daca newName este invalid
        """
        try:
            self.__validator.validateDisciplineName(newName)
        except InvalidNameError as err:
            raise InvalidNameError(str(err))

        try:
            discipline = self.__catalogue.findDisciplineByID(IDDiscipline)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))

        self.__catalogue.modifyDiscName(discipline, newName)


    def modifyTeacher(self, IDDiscipline, newFirstName, newLastName):
        """
        Modifica numele profesorului de la disciplina respectiva in newFirstName si newLastName
        :param IDDiscipline: id-ul disciplinei - string
        :param newFirstName: noul prenume - string
        :param newLastName: noul nume - string
        """
        try:
            self.__validator.validateTeacher(newFirstName, newLastName)
        except InvalidNameError as err:
            raise InvalidNameError(str(err))

        try:
            discipline = self.__catalogue.findDisciplineByID(IDDiscipline)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))

        self.__catalogue.modifyDiscTeacher(discipline, newFirstName, newLastName)

    def modifyOptional(self, IDDiscipline, isOptional):
        """
        Modifica caracterul disciplinei IDDiscipline
        :param IDDiscipline: id-ul disciplinei - string
        :param isOptional: caracterul disciplinei - boolean
        """
        try:
            discipline = self.__catalogue.findDisciplineByID(IDDiscipline)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))
        self.__catalogue.modifyDiscOptional(discipline, isOptional)

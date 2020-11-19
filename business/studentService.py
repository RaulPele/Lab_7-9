from domain.student import Student
from validation.errors import InvalidStudentError, StudentAlreadyExistsError
from validation.errors import InvalidIDError, NonExistentIDError
from validation.errors import InvalidNameError, NonExistentStudentError
import random
import string

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

    def getOptionals(self, IDStudent):
        """Returneaza lista de optionale selecate de studentul IDStudent
        :param IDStudent: id-ul studentului - string
        :return optionals: lista de optionale"""
        student = self.__catalogue.findStudentByID(IDStudent)
        return student.getOptionals()

    def removeStudent(self, identifier):
        """
        Sterge studentul identificat dupa identifier din catalog
        raise InvalidIDError - daca id-ul nu este valid
        raise NonExistentIDError - daca id-ul este valid dar nu se afla in lista studentilor
        :param identifier: identificator pentru student - string
        """
        try:
            self.__validator.validateID(identifier)
        except InvalidIDError as idErr:

            try:
                names = identifier.split(" ")
                self.__validator.validateName(names[0], names[1])
            except InvalidNameError:
                raise InvalidStudentError("Numele sau ID-ul studentului este invalid!\n")
            except IndexError:
                raise InvalidStudentError("Numele sau ID-ul studentului este invalid!\n")

            try:
                self.__catalogue.removeStudentByName(identifier)
            except NonExistentStudentError as err:
                raise NonExistentStudentError(str(err))
        else:
            try:
                self.__catalogue.removeStudentByID(identifier)
            except NonExistentStudentError as err:
                raise NonExistentStudentError(str(err))

    def findStudent(self, identifier):
        """
        Returneaza studentul/studentii identificati dupa identifier
        :param identifier: string - identificator pentru student
        :return: student - studentul corespunzator lui identifier sau lista de studenti
        """
        try:
            students = self.findStudentByID(identifier)
        except (InvalidStudentError, NonExistentStudentError):
            try:
                students = self.findStudentByName(identifier)
            except (NonExistentStudentError, InvalidStudentError):
                raise InvalidStudentError("Numele sau ID-ul studentului este invalid!\n")
            else:
                return students
            raise InvalidStudentError("Numele sau ID-ul studentului este invalid!\n")
        else:
            return students


    def findStudentByID(self, idStudent):
        try:
            self.__validator.validateID(idStudent)
        except InvalidIDError as err:
            raise InvalidStudentError(str(err))

        try:
            student = self.__catalogue.findStudentByID(idStudent)
        except NonExistentIDError as err:
            raise NonExistentStudentError(str(err))
        return student

    def findStudentByName(self, name):
        try:
            names = name.split(" ")
            self.__validator.validateName(names[0], names[1])
        except InvalidNameError:
            raise InvalidStudentError("Numele sau ID-ul studentului este invalid!\n")
        except IndexError:
            raise InvalidStudentError("Numele sau ID-ul studentului este invalid!\n")

        try:
            students = self.__catalogue.findStudentByName(name)
        except NonExistentStudentError as err:
            raise NonExistentStudentError(str(err))

        return students


    def modifyID(self, oldID, newID):
        """
        Modifica id-ul unui student in newID
        :param oldID: id-ul curent al studentului - string
        :param newID: noul id al studentului - string
        raise InvalidIDError - daca newID este invalid
        """
        try:
            self.__validator.validateID(newID)
        except InvalidIDError:
            raise InvalidIDError("ID-ul nou este invalid!\n")

        try:
            student = self.__catalogue.findStudentByID(oldID)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))

        self.__catalogue.modifyStudentID(student, newID)


    def modifyName(self, IDStudent, newFirstName, newLastName):
        """
        Modifica numele studentului IDStudent in newFirstName si newLastName
        :param IDStudent: id-ul studentului - string
        :param newFirstName: noul prenume al studentului - string
        :param newLastName: noul nume al studentului - string
        raise InvalidNameError daca newFirstName sau newLastName sunt invalide
        """
        try:
            self.__validator.validateName(newFirstName, newLastName)
        except InvalidNameError as err:
            raise InvalidNameError(str(err))

        try:
            student = self.__catalogue.findStudentByID(IDStudent)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))
        self.__catalogue.modifyStudentName(student, newFirstName, newLastName)

    def __generateRandomID(self):
        id = ""
        for i in range(0, 5):
            id += random.choice(string.digits)
        return id

    def __generateRandomName(self):
        name = ""
        for i in range(0, 4):
            name += random.choice(string.ascii_lowercase)
        return name

    def __isUnique(self, id):
        try:
            self.__catalogue.findStudentByID(id)
        except NonExistentIDError:
            return True
        return False

    def generateRandomStudents(self, numberOfStudents):
        try:
            self.__validator.validateNumber(numberOfStudents)
        except ValueError as err:
            raise ValueError(str(err))

        for i in range(0, numberOfStudents):
            id = self.__generateRandomID()
            while not self.__isUnique(id):
                id = self.__generateRandomID()

            firstName = self.__generateRandomName()
            lastName = self.__generateRandomName()

            student = Student(id, firstName, lastName)
            self.__catalogue.addStudent(student)



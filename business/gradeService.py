from validation.errors import NonExistentIDError, NonExistentStudentError, InvalidStudentError
from validation.errors import InvalidGradeError, InvalidIDError, InvalidNameError, NonExistentGradeError
from domain.grade import Grade
from data.DTOs.StudentPrintDTO import StudentPrintDTO

class GradeService:
    def __init__(self, gradesRepo, catalogue, discValidator, studValidator, gradeValidator):
        self.__gradesRepo = gradesRepo
        self.__catalogue = catalogue
        self.__discValidator = discValidator
        self.__studValidator = studValidator
        self.__gradeValidator = gradeValidator

    def addGrade(self, studIdentifier, discIdentifier, gradeValue):
        """
        Adauga o nota pentru studentul cu id-ul studIdentifier, la disciplina cu id-ul discIdentifier
        avand valoarea gradeValue in lista de note
        :param studIdentifier: id-ul studentului - string
        :param discIdentifier: id-ul disciplinei - string
        :param gradeValue: nota - float

        :raise:InvalidGradeError - daca valoarea notei este invalida
        :raise: InvalidIDError - daca id-ul studentului sau al disciplinei este invalid
        :raise: NonExistentIDError - daca disciplina cu id-ul dat nu exista
        """

        try:
            self.__gradeValidator.validateGrade(gradeValue)
        except InvalidGradeError as err:
            raise InvalidGradeError(str(err))

        try:
            self.__studValidator.validateID(studIdentifier)
            self.__discValidator.validateID(discIdentifier)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            self.__catalogue.findDisciplineByID(discIdentifier)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))

        grade = Grade(gradeValue, studIdentifier, discIdentifier)
        self.__gradesRepo.addGrade(grade)

    def removeGrade(self, studIdentifier, discIdentifier, gradeValue):
        """
        Sterge o nota pentru studentul studIdentifier, la disciplina discIdentifier cu valoarea gradeValue
        :param studIdentifier: id-ul studentului - string
        :param discIdentifier: id-ul disciplinei - string
        :param gradeValue: valoarea notei - float
        :raise: InvalidIDError - daca id-ul studentului sau al disciplinei este invalid
        :raise: InvalidGradeError - daca valoarea notei este invalida
        :raise: NonExistentIDError - daca disciplina cu id-ul dat nu exista
        """

        try:
            self.__studValidator.validateID(studIdentifier)
            self.__discValidator.validateID(discIdentifier)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            self.__gradeValidator.validateGrade(gradeValue)
        except InvalidGradeError as err:
            raise InvalidGradeError(str(err))

        try:
            self.__catalogue.findDisciplineByID(discIdentifier)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))

        try:
            self.__gradesRepo.removeGrade(Grade(gradeValue, studIdentifier, discIdentifier))
        except NonExistentGradeError as err:
            raise NonExistentGradeError(str(err))

    def getStudentInfoByID(self, studentID):
        try:
            self.__studValidator.validateID(studentID)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            student = self.__catalogue.findStudentByID(studentID)
        except NonExistentStudentError as err:
            raise NonExistentStudentError(str(err))

        grades = self.__gradesRepo.getAllForStudent(studentID)

        studentPrint = StudentPrintDTO(student, student.getDisciplines(), grades, self.__gradesRepo.getAverage(studentID))

        return studentPrint

    def getStudentInfoByName(self, studentName):
        try:
            names = studentName.split(" ")
            self.__studValidator.validateName(names[0], names[1])
        except (IndexError, KeyError, InvalidNameError) as err:
            raise InvalidNameError("Numele studentului este invalid!\n")

        try:
            students = self.__catalogue.findStudentByName(studentName)
        except NonExistentStudentError as err:
            raise NonExistentStudentError(str(err))

        return self.getStudentPrints(students)

    def getStudentInfo(self, identifier):
        try:
            studentPrints = self.getStudentInfoByID(identifier)
        except InvalidIDError:
            try:
                studentPrints = self.getStudentInfoByName(identifier)
            except InvalidNameError:
                raise InvalidStudentError("Numele sau id-ul studentului este invalid!\n")
            except NonExistentStudentError as err:
                raise NonExistentStudentError(str(err))

            return studentPrints
        except NonExistentStudentError as err:
            raise NonExistentStudentError(str(err))

        return studentPrints

    def getStudentPrints(self, students):
        studentPrints = []
        for student in students:
            grades = self.__gradesRepo.getAllForStudent(student.getID())
            studentPrints.append(StudentPrintDTO(student, student.getDisciplines(), grades, self.__gradesRepo.getAverage(student.getID())))

        return studentPrints
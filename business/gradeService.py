from validation.errors import NonExistentIDError, NonExistentStudentError, InvalidStudentError
from validation.errors import InvalidGradeError, InvalidIDError, InvalidNameError
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

    #TODO: testfunctions
    def getStudentInfoByName(self, studentName):
        try:
            names = studentName.split(" ")
            self.__studValidator.validateName(names[0], names[1])
        except (IndexError, KeyError, InvalidNameError) as err:
            raise InvalidNameError(str(err))

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
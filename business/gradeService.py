from validation.errors import NonExistentIDError, NonExistentStudentError
from validation.errors import InvalidGradeError, InvalidIDError
from domain.grade import Grade
from data.DTOs import StudentPrintDTO

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

        grade = Grade(gradeValue, studIdentifier, discIdentifier)
        self.__gradesRepo.addGrade(grade)

    def getStudentInfo(self, studentID):
        try:
            self.__studValidator.validateID(studentID)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            student = self.__catalogue.findStudentByID(studentID)
        except NonExistentStudentError as err:
            raise NonExistentStudentError(str(err))




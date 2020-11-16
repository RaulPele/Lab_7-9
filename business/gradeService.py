from validation.errors import NonExistentIDError
from validation.errors import InvalidGradeError, InvalidIDError
from domain.grade import Grade

class GradeService:
    def __init__(self, catalogue, discValidator, studValidator, gradeValidator):
        self.__catalogue = catalogue
        self.__discValidator = discValidator
        self.__studValidator = studValidator
        self.__gradeValidator = gradeValidator

    #TODO: refactor
    def assignGrade(self, studIdentifier, discIdentifier, gradeValue):
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

        try:
            self.__catalogue.assignGrade(grade)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))
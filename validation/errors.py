class StudentAlreadyExistsError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidStudentError(Exception):
    def __init__(self, message):
        super().__init__(message)

class InvalidDisciplineError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DisciplineAlreadyExistsError(Exception):
    def __init__(self, message):
        super().__init__(message)


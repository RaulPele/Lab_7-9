from ui.console import Console
from business.studentService import StudentService
from business.disciplineService import DisciplineService
from business.gradeService import GradeService
from data.repositories.catalogue import  Catalogue
from validation.validators import  StudentValidator, DisciplineValidator, GradeValidator
from tests.tests import Tests


if __name__ == "__main__":
    catalogue = Catalogue()
    studentValidator = StudentValidator()
    studentSrv = StudentService(catalogue, studentValidator)
    disciplineValidator = DisciplineValidator()
    disciplineSrv = DisciplineService(catalogue, disciplineValidator)
    gradeValidator = GradeValidator()
    gradeSrv = GradeService(catalogue, disciplineValidator, studentValidator, gradeValidator)

    console = Console(studentSrv, disciplineSrv, gradeSrv)
    tests = Tests()
    tests.runTests()
    console.run()





from ui.console import Console
from business.studentService import StudentService
from business.disciplineService import DisciplineService
from business.gradeService import GradeService
from data.repositories.catalogue import  Catalogue
from data.repositories.catalogueFileRepo import CatalogueFileRepository
from data.repositories.GradesRepository import GradesRepository
from data.repositories.GradesFileRepo import GradesFileRepository
from validation.validators import  StudentValidator, DisciplineValidator, GradeValidator
from tests.tests import Tests
import unittest

if __name__ == "__main__":
    #catalogue = Catalogue()
    catalogue = CatalogueFileRepository("students.txt", "disciplines.txt")
   #gradesRepo = GradesRepository()
    gradesRepo = GradesFileRepository()
    studentValidator = StudentValidator()
    studentSrv = StudentService(catalogue, studentValidator)
    disciplineValidator = DisciplineValidator()
    disciplineSrv = DisciplineService(catalogue, gradesRepo,  disciplineValidator)
    gradeValidator = GradeValidator()

    gradeSrv = GradeService(gradesRepo,catalogue, disciplineValidator, studentValidator, gradeValidator)

    console = Console(studentSrv, disciplineSrv, gradeSrv)
    #tests = Tests()
    #tests.runTests()
    console.run()






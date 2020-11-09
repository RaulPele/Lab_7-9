from ui.console import Console
from business.services import StudentSrv, DisciplineService
from data.repositories.catalogue import  Catalogue
from validation.validators import  StudentValidator, DisciplineValidator

if __name__ == "__main__":
    catalogue = Catalogue()
    studentValidator = StudentValidator()
    studentSrv = StudentSrv(catalogue, studentValidator)
    disciplineValidator = DisciplineValidator()
    disciplineSrv = DisciplineService(catalogue, disciplineValidator)
    console = Console(studentSrv, disciplineSrv)
    console.run()
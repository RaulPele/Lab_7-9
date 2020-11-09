from ui.console import Console
from business.services import StudentSrv, DisciplineService
from data.repositories.catalogue import  Catalogue
from validation.validators import  StudentValidator, DisciplineValidator

class test:
    def f(self):
        print("hello")

if __name__ == "__main__":
    catalogue = Catalogue()
    studentValidator = StudentValidator()
    studentSrv = StudentSrv(catalogue, studentValidator)
    disciplineValidator = DisciplineValidator()
    disciplineSrv = DisciplineService(catalogue, disciplineValidator)
    console = Console(studentSrv, disciplineSrv)
    console.run()
    #test1 = test()
    #list = [test]
    #del list[0]
    #test1.f()



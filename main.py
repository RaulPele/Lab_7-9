from ui.console import Console
from business.services import StudentSrv
from data.catalogue import  Catalogue
from validation.validators import  StudentValidator

if __name__ == "__main__":
    catalogue = Catalogue()
    studentValidator = StudentValidator()
    studentSrv = StudentSrv(catalogue, studentValidator)
    console = Console(studentSrv)
    console.run()
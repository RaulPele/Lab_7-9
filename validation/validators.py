from validation.errors import  InvalidStudentError, InvalidDisciplineError, InvalidIDError
from validation.errors import InvalidNameError, InvalidOptional

class StudentValidator:

    def validateStudent(self, student):
        """
        Valideaza studentul student
        raise InvalidStudentError(mesaj) - daca unul din campuri nu este valid
        mesaje posibile: "ID-ul studentului este invalid! \n", "Prenumele studentului este invalid!\n"
        "Numele studentului este invalid!\n"
        :param student: studentul pentru care se face validarea (tip Student())

        """
        id = student.getID()
        firstName = student.getFirstName()
        lastName = student.getLastName()
        errors =""
        try:
            self.validateID(id)
        except InvalidIDError as err:
            errors+= str(err)

        try:
            self.validateName(firstName, lastName)
        except InvalidNameError as err:
            errors += str(err)

        if len(errors) != 0:
            raise InvalidStudentError(errors)

    def validateID(self, id):
        if not id.isnumeric():
            raise InvalidIDError("ID-ul studentului este invalid! \n")

    def validateName(self, firstName, lastName):
        errors=""
        for name in firstName.split("-"):
            if not name.isalpha():

                errors += "Prenumele studentului este invalid!\n"
                break

        if not lastName.isalpha():
            errors += "Numele studentului este invalid!\n"

        if len(errors) != 0:
            raise InvalidNameError(errors)




class DisciplineValidator:

    def validateDiscipline(self, discipline):
        id = discipline.getID()
        name = discipline.getName()
        teacherFirst = discipline.getTeacherFirst()
        teacherLast = discipline.getTeacherLast()
        isOptional = discipline.getIsOptional()

        errors = ""
        try:
            self.validateID(id)
        except InvalidIDError as err:
            errors += str(err)

        try:
            self.validateDisciplineName(name)
        except InvalidNameError as err:
            errors += str(err)

        try:
            self.validateTeacher(teacherFirst, teacherLast)
        except InvalidNameError as err:
            errors +=str(err)

        try:
            self.validateOptional(isOptional)
        except InvalidOptional as err:
            errors +=str(err)

        if len(errors)!=0:
            raise InvalidDisciplineError(errors)

    def validateID(self, id):
        if not id.isnumeric():
            raise InvalidIDError("ID-ul disciplinei este invalid! \n")

    def validateTeacher(self, firstName, lastName):
        errors = ""

        for name in firstName.split("-"):
            if not name.isalpha():
                errors += "Prenumele profesorului este invalid!\n"
                break

        if not lastName.isalpha():
            errors += "Numele profesorului este invalid!\n"

        if len(errors) != 0:
            raise InvalidNameError(errors)

    def validateDisciplineName(self, name):
        for n in name.split(" "):
            if not n.isalpha():
                raise InvalidNameError("Numele disciplinei este invalid!\n")

    def validateOptional(self, isOptional):
        if isOptional not in [True, False]:
            raise InvalidOptional("Nu a fost specificat caracterul disciplinei (optional sau obligatoriu)!\n")
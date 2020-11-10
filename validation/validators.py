from validation.errors import  InvalidStudentError, InvalidDisciplineError, InvalidIDError
from validation.errors import InvalidNameError, InvalidOptional, InvalidGradeError

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
        """
        Valideaza id-ul id
        :param id: string - id
        raise InvalidIDError- daca id-ul este invalid
        """
        if not id.isnumeric():
            raise InvalidIDError("ID-ul studentului este invalid!\n")

    def validateName(self, firstName, lastName):
        """
        Valideaza numele unui student
        :param firstName: prenume - string
        :param lastName: nume - string
        raise InvalidNameError - daca numele nu este valid
        """
        errors=""
        for name in firstName.split("-"):
            if not name.isalpha():

                errors += "Prenumele studentului este invalid!\n"
                break

        if not lastName.isalpha():
            errors += "Numele studentului este invalid!\n"

        if len(errors) != 0:
            raise InvalidNameError(errors)

    def validateGrade(self, grade):
        if grade<1 or grade > 10:
            raise InvalidGradeError("Nota trebuie as fie un numar real intre 1 si 10!\n")




class DisciplineValidator:

    def validateDiscipline(self, discipline):
        """
        Validaeza o disciplina
        :param discipline: obiect Discipline()
        raise InvalidDisciplineError - daca unul din campurile obiectului discipline nu este valid
        """
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
        """
        Validaeza id-ul unei discipline
        :param id: id- string
        raise InvalidIDError - daca id-ul nu este valid
        """
        if not id.isnumeric():
            raise InvalidIDError("ID-ul disciplinei este invalid!\n")

    def validateTeacher(self, firstName, lastName):
        """
        Valideaza numele unui profesor corespunzator unei discipline
        :param firstName: prenume - string
        :param lastName: nume - string
        raise InvalidNameError - daca numele nu este valid
        """
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
        """
        Valideaza numele unei discipline
        :param name: nume - string
        raise InvalidNameError - daca numele nu este valid
        """
        for n in name.split(" "):
            if not n.isalpha():
                raise InvalidNameError("Numele disciplinei este invalid!\n")

    def validateOptional(self, isOptional):
        """
        Validaeza campul isOptional al unei discipline
        :param isOptional: boolean
        raise InvalidOptional - daca valoarea variabilei nu este de tip boolean
        """
        if isOptional not in [True, False]:
            raise InvalidOptional("Nu a fost specificat caracterul disciplinei (optional sau obligatoriu)!\n")
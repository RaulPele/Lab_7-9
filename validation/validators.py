from validation.errors import  InvalidStudentError, InvalidDisciplineError

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
        if not id.isnumeric():
            errors += "ID-ul studentului este invalid! \n"

        for name in firstName.split("-"):
            if not name.isalpha():

                errors += "Prenumele studentului este invalid!\n"
                break

        if not lastName.isalpha():
            errors += "Numele studentului este invalid!\n"

        if len(errors) != 0:
            raise InvalidStudentError(errors)

class DisciplineValidator:

    def validateDiscipline(self, discipline):
        id = discipline.getID()
        name = discipline.getName()
        teacherFirst = discipline.getTeacherFirst()
        teacherLast = discipline.getTeacherLast()
        isOptional = discipline.getIsOptional()

        errors = ""
        if not id.isnumeric():
            errors += "ID-ul disciplinei este invalid!\n"

        for n in name.split(" "):
            if not n.isalpha():
                errors += "Numele disciplinei este invalid!\n"
                break

        if not teacherLast.isalpha():
            errors += "Numele profesorului disciplinei este invalid!\n"

        for firstName in teacherFirst.split("-"):
            if not firstName.isalpha():
                errors += "Prenumele profesorului este invalid!\n"
                break

        if isOptional not in [True, False]:
            errors += "Nu a fost specificat caracterul disciplinei (optional sau obligatoriu)!\n"

        if len(errors)!=0:
            raise InvalidDisciplineError(errors)

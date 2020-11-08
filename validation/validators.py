from validation.errors import  InvalidStudentError

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

        if not firstName.isalpha():
            errors += "Prenumele studentului este invalid!\n"

        if not lastName.isalpha():
            errors += "Numele studentului este invalid!\n"

        if len(errors) != 0:
            raise InvalidStudentError(errors)

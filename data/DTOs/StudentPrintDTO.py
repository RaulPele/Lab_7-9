from utils.colors import Colors


class StudentPrint:
    def __init__(self, student, disciplines, grades):
        self.__student = student
        self.__disciplines = disciplines
        self.__grades = grades

    def __str__(self):
        output = str(self.__student) + '\n'
        for d in self.__disciplines:
            output += str(d) + self.__getGrades(d) +"\n"
        output += Colors.RESET

    def __getGrades(self, discipline):
        discGrades=[]
        for grade in self.__grades:
            if grade.getDisciplineID() == discipline.getID():
                discGrades.append(grade.getValue())

        gradeStr = Colors.GREEN + str(discGrades)

        return gradeStr

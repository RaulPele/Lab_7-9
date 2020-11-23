from utils.colors import Colors


class StudentPrintDTO:
    def __init__(self, student, disciplines, grades, average):
        self.__student = student
        self.__disciplines = disciplines
        self.__grades = grades
        self.__average = average

    def __str__(self):
        output = str(self.__student)
        output += Colors.RED + "Medie generala: " + Colors.GREEN+ str(self.__average) +'\n\n' + Colors.RESET
        for d in self.__disciplines:
            output += str(d) + self.__getGrades(d) +"\n\n"
        output += Colors.RESET
        return output

    def __getGrades(self, discipline):
        discGrades=[]
        for grade in self.__grades:
            if grade.getDisciplineID() == discipline.getID():
                discGrades.append(grade.getValue())

        gradeStr = Colors.GREEN + str(discGrades)

        return gradeStr


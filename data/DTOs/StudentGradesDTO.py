from utils.colors import Colors
class StudentGradesDTO:
    def __init__(self, student, grades, average):
        self.__student = student
        self.__grades = grades
        self.__average = average

    def __str__(self):
        output = str(self.__student)
        gradeValues =[]
        for grade in self.__grades:
            gradeValues.append(grade.getValue())
        output += Colors.RED + "Note: " + Colors.GREEN + str(gradeValues) + Colors.RESET + "\n"
        output += Colors.RED+"Medie: " + Colors.GREEN + str(self.__average) + Colors.RESET +'\n'

        return output

    def __eq__(self, other):
        return self.__student == other.__student and self.__grades == other.__grades

    def getAverage(self):
        return self.__average
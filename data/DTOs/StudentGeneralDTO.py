from utils.colors import Colors

class StudentGeneralDTO:
    def __init__(self, student, average):
        self.__student = student
        self.__average = average

    def __str__(self):
        output = str(self.__student)
        output += Colors.RED + "Medie generala: "+ self.__average +Colors.RESET +'\n'
        return output

    def getAverage(self):
        return self.__average

    def __eq__(self, other):
        return self.__student == other.__student and self.__average == other.__average
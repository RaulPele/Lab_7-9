class GradesRepository:
    def __init__(self):
        self.__grades = []

    def addGrade(self, grade):
        self.__grades.append(grade)

    #TODO: testGetAverage
    def getAverage(self, studentID):
        """
        Calculeaza media generala pentru un student
        :param studentID: id-ul studentului
        :return: 0, daca studentul nu are note
        :return: media studentului - float
        """
        sum = 0
        numOfDisc = 0

        for grade in self.__grades:
            if grade.getStudentID() == studentID:
                sum += grade.getValue()
                numOfDisc += 1

        if numOfDisc == 0:
            return 0
        return sum/numOfDisc


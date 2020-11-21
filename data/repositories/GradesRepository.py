from validation.errors import  NonExistentIDError, NonExistentDisciplineError

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

    def getAllForStudent(self, studentID):
        """
        Returneaza toate notele unui student la toate disciplnele
        :param studentID: id-ul studentului - string
        :return studGrades: lista de note -Grade()
        """
        studGrades = []
        for grade in self.__grades:
            if grade.getStudentID() == studentID:
                studGrades.append(grade)

        return studGrades

    def removeDisciplineGradesByID(self, disciplineID):
        i=0
        disciplinesDeleted = False
        while i<len(self.__grades):
            grade = self.__grades[i]
            if grade.getDisciplineID() == disciplineID:
                del self.__grades[i]
                disciplinesDeleted = True
                continue
            i+=1

        if not disciplinesDeleted:
            raise NonExistentIDError("Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n")


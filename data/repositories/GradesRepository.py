from validation.errors import  NonExistentIDError, NonExistentGradeError

class GradesRepository:
    def __init__(self):
        self.__grades = []

    def addGrade(self, grade):
        self.__grades.append(grade)

    def removeGrade(self, grade):
        """
        Sterge o nota din lista de note
        :param grade: nota care se va sterge - Grade
        raise NonExistentGradeError: daca nu exista nota cu id-ul dat
        """
        for i in range (0, len(self.__grades)):
            if self.__grades[i] == grade:
                del self.__grades[i]
                return
        raise NonExistentGradeError("Nota nu se afla in lista de note!\n")


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
        """
        Sterge toate notele corespunzatoare unei discipline cu id-ul disciplineID
        :param disciplineID: id-ul disciplinei - string
        """
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

    def getAllGrades(self):
        return self.__grades
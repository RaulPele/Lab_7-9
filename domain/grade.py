class Grade:
    def __init__(self, value = 0, IDStudent =None, IDDiscipline=None):
        self.__value = value
        self.__IDStudent = IDStudent
        self.__IDDiscipline = IDDiscipline

    def getValue(self):
        return self.__value

    def getStudentID(self):
        return self.__IDStudent

    def getDisciplineID(self):
        return self.__IDDiscipline


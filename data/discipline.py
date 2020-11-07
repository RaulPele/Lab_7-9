class Discipline:
    def __init__(self, IDDiscipline, name, teacher, isOptional = True):
        self.__IDDiscipline = IDDiscipline
        self.__name = name
        self.__teacher = teacher
        self.__isOptional = isOptional


    def getID(self):
        return self.__IDDiscipline

    def getName(self):
        return self.__name

    def getTeacher(self):
        return self.__teacher

    def setID(self, ID):
        self.__IDDiscipline = ID

    def setName(self, name):
        self.__name = name

    def setTeacher(self, teacher):
        self.__teacher = teacher

    def setOptional(self, isOptional):
        self.__isOptional = isOptional
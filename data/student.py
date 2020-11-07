class Student:
    def __init__(self, IDStudent, firstName, lastName):
        self.__IDStudent = IDStudent
        self.__firstName = firstName
        self.__lastName = lastName
        self.__genAverage = 0
        self.__disciplines = []

    def getID(self):
        return self.__IDStudent

    def getName(self):
        return self.__firstName + " " + self.__lastName

    def getAverage(self):
        return self.__genAverage

    def getDisciplines(self):
        return self.__disciplines

    def setID(self, ID):
        self.__IDStudent = ID

    def setName(self, firstName, lastName):
        self.__firstName = firstName
        self.__lastName = lastName

    def setFirstName(self, firstName):
        self.__firstName = firstName

    def setLastName(self, lastName):
        self.__lastName = lastName



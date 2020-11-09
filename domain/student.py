class Student:
    def __init__(self, IDStudent, firstName, lastName):
        self.__IDStudent = IDStudent
        self.__firstName = firstName
        self.__lastName = lastName
        self.__genAverage = 0
        self.__disciplines = []
        self.formatName()

    def getID(self):
        return self.__IDStudent

    def getName(self):
        return self.__firstName + " " + self.__lastName

    def getFirstName(self):
        return self.__firstName

    def getLastName(self):
        return self.__lastName

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

    def __eq__(self, other):
        if self.__IDStudent == other.__IDStudent:
            return True
        return False

    def addDiscipline(self, discipline):
        """
        Adauga o noua disciplina pentru studentul self
        :param discipline: obiect Discipline
        """
        for i in range(0, len(self.__disciplines)):
            currentDiscipline = self.__disciplines[i]
            if discipline.getName() >currentDiscipline.getName():
                self.__disciplines.insert(i+1, discipline)
                break

    def formatName(self):
        if(self.__firstName.isalpha()):
            self.__firstName = self.__firstName.capitalize()
        if self.__lastName.isalpha():
            self.__lastName =self.__lastName.capitalize()
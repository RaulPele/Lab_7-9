from utils.colors import Colors
class Student:
    def __init__(self, IDStudent, firstName, lastName):
        self.__IDStudent = IDStudent
        self.__firstName = firstName
        self.__lastName = lastName
        self.__genAverage = 0
        self.__disciplines = []
        self.__grades = {}
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

    def getGrade(self, discipline):
        return self.__grades[discipline.getID()]

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

    def __str__(self):
        output = Colors.RED + "ID: " + Colors.GREEN + self.getID() + '\n' +\
                Colors.RED + "Nume: " + Colors.GREEN + self.getLastName() + "\n"+\
                Colors.RED + "Prenume: " + Colors.GREEN + self.getFirstName() + "\n"+\
                Colors.RED + "Medie generala: " + Colors.GREEN + str(self.getAverage()) + "\n\n"
        for discipline in self.getDisciplines():
            output += str(discipline)
            output+= Colors.RED +"Note: " + Colors.GREEN + str(self.getGrade(discipline)) + "\n\n"
        output+=Colors.RESET
        return output


    def addDiscipline(self, discipline):
        """
        Adauga o noua disciplina pentru studentul self
        :param discipline: obiect Discipline
        """
        if len(self.__disciplines) ==0:
            self.__disciplines.append(discipline)
            self.addGrade(discipline, 0)
            return

        oldSize = len(self.__disciplines)
        for i in range(0, len(self.__disciplines)):
            currentDiscipline = self.__disciplines[i]
            if discipline.getName() <currentDiscipline.getName():
                self.__disciplines.insert(i, discipline)
                break

        if oldSize == len(self.__disciplines):
            self.__disciplines.append(discipline)
        self.addGrade(discipline, 0)

    def removeDiscipline(self, discipline):
        """
        Sterge disciplina discipline din lista studentului de discipline
        si sterge notele aferente disciplinei
        :param discipline: obiect Discipline()
        """
        if discipline in self.__disciplines:
            for i in range(0, len(self.__disciplines)):
                if self.__disciplines[i] == discipline:
                    del self.__disciplines[i]
                    del self.__grades[discipline.getID()]
                    self.__calculateAverage()
                    return

    def addGrade(self, discipline, grade):
        """
        Adauga o nota la disciplina discipline
        :param discipline: disciplina Discipline()
        :param grade: nota - int
        """
        if discipline.getID() not in self.__grades.keys():
            self.__grades[discipline.getID()] = []
        else:
            self.__grades[discipline.getID()].append(grade)
            self.__calculateAverage()

    def __calculateAverage(self):
        sum = 0
        numOfGrades = 0
        for list in self.__grades.values():
            for grade in list:
                sum +=grade
                numOfGrades +=1
        if numOfGrades!=0:
            self.__genAverage = sum/numOfGrades
        else:
            self.__genAverage = 0

    def makeCopy(self):
        copy = Student(self.getID(), self.getFirstName(), self.getLastName())
        return copy



    def formatName(self):
        """
        Formateaza campurile studentului
        Capitalizeaza numele si prenumele studentului
        """
        formatedFirstName=""

        for name in self.__firstName.split("-"):
            formatedFirstName += name.capitalize()
            formatedFirstName +="-"

        formatedFirstName = formatedFirstName[0:len(formatedFirstName)-1]
        self.__firstName = formatedFirstName
        self.__lastName = self.__lastName.capitalize()
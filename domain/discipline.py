from utils.colors import  Colors
class Discipline:
    def __init__(self, IDDiscipline, name, teacherFirst, teacherLast, isOptional = "Da"):
        self.__IDDiscipline = IDDiscipline
        self.__name = name
        self.__teacherFirst = teacherFirst
        self.__teacherLast = teacherLast
        self.__isOptional = isOptional
        self.formatFields()


    def getID(self):
        return self.__IDDiscipline

    def getName(self):
        return self.__name

    def getTeacher(self):
        return self.__teacherFirst + " "+ self.__teacherLast

    def getTeacherFirst(self):
        return self.__teacherFirst

    def getTeacherLast(self):
        return self.__teacherLast

    def getIsOptional(self):
        return self.__isOptional

    def setID(self, ID):
        self.__IDDiscipline = ID

    def setName(self, name):
        self.__name = name

    def setTeacherFirst(self, firstName):
        self.__teacherFirst = firstName

    def setTeacherLast(self, lastName):
        self.__teacherLast = lastName

    def setOptional(self, isOptional):
        self.__isOptional = isOptional

    def __eq__(self, other):
        if self.__IDDiscipline == other.__IDDiscipline:
            return True
        if self.__name == other.__name and self.getTeacher() == other.getTeacher():
            return True
        return False

    def __str__(self):
        output = Colors.RED + "ID: "+ Colors.GREEN + self.getID() +"\n"+\
                 Colors.RED + "Nume: " + Colors.GREEN + self.getName() + "\n"+\
                 Colors.RED + "Profesor: " + Colors.GREEN + self.getTeacher() +"\n"

        if self.getIsOptional():
            output += Colors.GREEN + "Optional" +"\n"
        output += Colors.RESET

        return output


    def formatFields(self):
        formatedName=""
        for n in self.__name.split(" "):
            n = n.capitalize()
            formatedName += n
            formatedName += " "

        self.__name = formatedName.strip()

        formatedTFirstName=""
        for name in self.__teacherFirst.split("-"):
            name = name.capitalize()
            formatedTFirstName +=name
            formatedTFirstName += "-"

        self.__teacherFirst = formatedTFirstName[0:len(formatedTFirstName)-1]

        self.__teacherLast = self.__teacherLast.capitalize()

        if self.__isOptional.lower() == "da":
            self.__isOptional = True
        elif self.__isOptional.lower() =="nu":
            self.__isOptional = False

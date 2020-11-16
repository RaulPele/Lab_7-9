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
        self.__name = self.formatName()

    def setTeacherFirst(self, firstName):
        self.__teacherFirst = firstName
        self.__teacherFirst = self.formatTeacherFirst()

    def setTeacherLast(self, lastName):
        self.__teacherLast = lastName.capitalize()

    def setOptional(self, isOptional):
        self.__isOptional = isOptional
        self.formatOptional()

    def __eq__(self, other):
        "Defineste operatia de egalitate dintre doua obiecte de tip discipline"
        if self.__IDDiscipline == other.__IDDiscipline:
            return True
        if self.__name == other.__name and self.getTeacher() == other.getTeacher():
            return True
        return False

    def __str__(self):
        "Defineste modul in care se afiseaza obiectul sub forma de string"
        output = Colors.RED + "ID: "+ Colors.GREEN + self.getID() +"\n"+\
                 Colors.RED + "Nume: " + Colors.GREEN + self.getName() + "\n"+\
                 Colors.RED + "Profesor: " + Colors.GREEN + self.getTeacher() +"\n"

        if self.getIsOptional():
            output += Colors.GREEN + "Optional" +"\n"
        output += Colors.RESET

        return output

    def formatName(self):
        formatedName = ""
        for n in self.__name.split(" "):
            n = n.capitalize()
            formatedName += n
            formatedName += " "
        return formatedName.strip()

    def formatTeacherFirst(self):
        formatedTFirstName = ""
        for name in self.__teacherFirst.split("-"):
            name = name.capitalize()
            formatedTFirstName += name
            formatedTFirstName += "-"
        return formatedTFirstName[0:len(formatedTFirstName)-1]

    def formatOptional(self):
        if isinstance(self.__isOptional, str):
            if self.__isOptional.lower() == "da":
                self.__isOptional = True
            elif self.__isOptional.lower() =="nu":
                self.__isOptional = False

    def formatFields(self):
        "Formateaza campurile disciplinei capitalizand numele si transformand isOptional in boolean"

        self.__name = self.formatName()

        self.__teacherFirst = self.formatTeacherFirst()

        self.__teacherLast = self.__teacherLast.capitalize()

        self.formatOptional()

    def makeCopy(self):
        copy = Discipline(self.getID(), self.getName(), self.getTeacherFirst(), self.getTeacherFirst(), self.getIsOptional())
        return copy
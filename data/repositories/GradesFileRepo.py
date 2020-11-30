from data.repositories.GradesRepository import GradesRepository
from domain.grade import Grade

class GradesFileRepository(GradesRepository):
    def __init__(self):
        super().__init__()
        self.__gradesFileName = "grades.txt"

        self.__loadGradesFromFile()

    def __readGradeFromFile(self, line):
        attr = line.split(",")
        grade = Grade(float(attr[0]), attr[1], attr[2])

        return grade

    def __loadGradesFromFile(self):
        try:
            gradesFile = open(self.__gradesFileName, "r")
        except IOError as err:
            return

        for line in gradesFile:
            line = line.strip()
            if line == "":
                continue
            grade = self.__readGradeFromFile(line)
            super().addGrade(grade)

        gradesFile.close()

    def __appendGrade(self, grade):
        #value,IDStudent,IDDiscipline
        gradeStr = str(grade.getValue()) + "," + grade.getStudentID() + "," + grade.getDisciplineID()
        gradeStr += "\n"

        with open(self.__gradesFileName, "a") as gradesFile:
            gradesFile.write(gradeStr)

    def addGrade(self, grade):
        super().addGrade(grade)
        self.__appendGrade(grade)

    def __storeAllGrades(self):
        with open(self.__gradesFileName, "w") as gradesFile:
            for grade in self.getAllGrades():
                gradeStr = str(grade.getValue()) + "," + grade.getStudentID() + "," + grade.getDisciplineID()
                gradeStr += "\n"
                gradesFile.write(gradeStr)

    def removeGrade(self, grade):
        super().removeGrade(grade)
        self.__storeAllGrades()

    def removeDisciplineGradesByID(self, disciplineID):
        super().removeDisciplineGradesByID(disciplineID)
        self.__storeAllGrades()

from validation.errors import NonExistentIDError, NonExistentStudentError, InvalidStudentError
from validation.errors import InvalidGradeError, InvalidIDError, InvalidNameError, NonExistentGradeError
from validation.errors import NonExistentDisciplineError
from domain.grade import Grade
from data.DTOs.StudentPrintDTO import StudentPrintDTO
from data.DTOs.StudentGradesDTO import StudentGradesDTO
from data.DTOs.StudentGeneralDTO import StudentGeneralDTO
from utils.sorting import mergeSort, bingoSort

class GradeService:
    def __init__(self, gradesRepo, catalogue, discValidator, studValidator, gradeValidator):
        self.__gradesRepo = gradesRepo
        self.__catalogue = catalogue
        self.__discValidator = discValidator
        self.__studValidator = studValidator
        self.__gradeValidator = gradeValidator

    def addGrade(self, studIdentifier, discIdentifier, gradeValue):
        """
        Adauga o nota pentru studentul cu id-ul studIdentifier, la disciplina cu id-ul discIdentifier
        avand valoarea gradeValue in lista de note
        :param studIdentifier: id-ul studentului - string
        :param discIdentifier: id-ul disciplinei - string
        :param gradeValue: nota - float

        :raise:InvalidGradeError - daca valoarea notei este invalida
        :raise: InvalidIDError - daca id-ul studentului sau al disciplinei este invalid
        :raise: NonExistentIDError - daca disciplina cu id-ul dat nu exista
        """

        try:
            self.__gradeValidator.validateGrade(gradeValue)
        except InvalidGradeError as err:
            raise InvalidGradeError(str(err))

        try:
            self.__studValidator.validateID(studIdentifier)
            self.__discValidator.validateID(discIdentifier)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            discipline = self.__catalogue.findDisciplineByID(discIdentifier)
            student = self.__catalogue.findStudentByID(studIdentifier)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))

        if discipline.getIsOptional():
            if discipline not in student.getOptionals():
                raise NonExistentIDError("Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n")

        grade = Grade(gradeValue, studIdentifier, discIdentifier)
        self.__gradesRepo.addGrade(grade)

    def removeGrade(self, studIdentifier, discIdentifier, gradeValue):
        """
        Sterge o nota pentru studentul studIdentifier, la disciplina discIdentifier cu valoarea gradeValue
        :param studIdentifier: id-ul studentului - string
        :param discIdentifier: id-ul disciplinei - string
        :param gradeValue: valoarea notei - float
        :raise: InvalidIDError - daca id-ul studentului sau al disciplinei este invalid
        :raise: InvalidGradeError - daca valoarea notei este invalida
        :raise: NonExistentIDError - daca disciplina cu id-ul dat nu exista
        """

        try:
            self.__studValidator.validateID(studIdentifier)
            self.__discValidator.validateID(discIdentifier)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            self.__gradeValidator.validateGrade(gradeValue)
        except InvalidGradeError as err:
            raise InvalidGradeError(str(err))

        try:
            self.__catalogue.findDisciplineByID(discIdentifier)
            self.__catalogue.findStudentByID(studIdentifier)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))

        try:
            self.__gradesRepo.removeGrade(Grade(gradeValue, studIdentifier, discIdentifier))
        except NonExistentGradeError as err:
            raise NonExistentGradeError(str(err))

    def getStudentInfoByID(self, studentID):
        try:
            self.__studValidator.validateID(studentID)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            student = self.__catalogue.findStudentByID(studentID)
        except NonExistentStudentError as err:
            raise NonExistentStudentError(str(err))

        grades = self.__gradesRepo.getAllForStudent(studentID)

        studentPrint = StudentPrintDTO(student, student.getDisciplines(), grades, self.__gradesRepo.getAverage(studentID))

        return studentPrint

    def getStudentInfoByName(self, studentName):
        try:
            names = studentName.split(" ")
            self.__studValidator.validateName(names[0], names[1])
        except (IndexError, KeyError, InvalidNameError) as err:
            raise InvalidNameError("Numele studentului este invalid!\n")

        try:
            students = self.__catalogue.findStudentByName(studentName)
        except NonExistentStudentError as err:
            raise NonExistentStudentError(str(err))

        return self.getStudentPrints(students)

    def getStudentInfo(self, identifier):
        try:
            studentPrints = self.getStudentInfoByID(identifier)
        except InvalidIDError:
            try:
                studentPrints = self.getStudentInfoByName(identifier)
            except InvalidNameError:
                raise InvalidStudentError("Numele sau id-ul studentului este invalid!\n")
            except NonExistentStudentError as err:
                raise NonExistentStudentError(str(err))

            return studentPrints
        except NonExistentStudentError as err:
            raise NonExistentStudentError(str(err))

        return studentPrints

    def getStudentPrints(self, students):
        studentPrints = []
        for student in students:
            grades = self.__gradesRepo.getAllForStudent(student.getID())
            studentPrints.append(StudentPrintDTO(student, student.getDisciplines(), grades, self.__gradesRepo.getAverage(student.getID())))

        return studentPrints

    def getStudentsFromDiscipline(self, disciplineID):
        """
        Returneaza toti studentii cu notele lor de la o anumita disciplina
        :param disciplineID: id-ul disciplinei - string
        :return studentGradesDTOS: lista de dto-uri continand studentii si notele lor la o materie
        """
        try:
            self.__discValidator.validateID(disciplineID)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))

        try:
            self.__catalogue.findDisciplineByID(disciplineID)
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))

        studentGradesDTOS = []

        discipline = self.__catalogue.findDisciplineByID(disciplineID)
        for student in self.__catalogue.getStudents():
            if discipline in student.getDisciplines():
                discGrades = self.__gradesRepo.getDisciplineGrades(student.getID(), disciplineID)
                average = self.__gradesRepo.getAverageForDisc(student.getID(), disciplineID)
                newDto = StudentGradesDTO(student, discGrades, average)
                studentGradesDTOS.append(newDto)

        if len(studentGradesDTOS) == 0:
            raise NonExistentStudentError("Nu exista studenti inrolati la disciplina respectiva!\n")

        return studentGradesDTOS

    def getStudentsFromDisciplineSortedByAvg(self, disciplineID):
        """
        Returneaza toti studentii cu notele lor de la o anumita disciplina
        :param disciplineID: id-ul disciplinei - string
        :return studentGradesDTOS: lista de dto-uri continand studentii si notele lor la o materie
                                sortata dupa medie
        """
        try:
            studentGradesDTOS = self.getStudentsFromDiscipline(disciplineID)
        except InvalidIDError as err:
            raise InvalidIDError(str(err))
        except NonExistentStudentError as err:
            raise NonExistentStudentError(str(err))
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))

        #mergeSort(studentGradesDTOS, 0, len(studentGradesDTOS), key=lambda dto: dto.getAverage(), reverse=True)
        bingoSort(studentGradesDTOS, key=lambda dto: dto.getAverage(), reverse=True)

        return studentGradesDTOS

    def getTop20Percent(self):
        """
        Returneaza o lista de StudentGeneralDTO's continand primii 20% studenti luati dupa
        media generala
        :return: studentGeneralDTOS
        """
        studNumber = int((1/5) * len(self.__catalogue.getStudents()))

        studentGeneralDTOS =[]
        for student in self.__catalogue.getStudents():
            newDTO = StudentGeneralDTO(student, self.__gradesRepo.getAverage(student.getID()))
            studentGeneralDTOS.append(newDTO)

        if len(studentGeneralDTOS) == 0:
            raise NonExistentStudentError("Nu exista studenti in lista studentilor!\n")

        bingoSort(studentGeneralDTOS, key=lambda dto: dto.getAverage(), reverse=True)

        if studNumber ==0:
            raise NonExistentStudentError("Nu exista suficienti studenti in lista!\n")
        return studentGeneralDTOS[:studNumber]

    def __halfPromoted(self, studentGradeDTOS):
        total = len(studentGradeDTOS)
        promoted = 0
        for student in studentGradeDTOS:
            if student.getAverage() >5:
                promoted +=1
        if promoted >= total/2:
            return True
        return False

    def __filterStudents(self, studentGradesDTOS, discipline):
        studentGradesDTOS = [stud for stud in studentGradesDTOS if discipline in stud.getStudent().getDisciplines()]
        return studentGradesDTOS

    def getPromotingDisciplines(self):
        promotedDisciplines =[]
        disciplines = self.__catalogue.getDisciplines()

        for discipline in disciplines:
            studentGradesDTOS = self.getStudentsFromDisciplineSortedByAvg(discipline.getID())
            studentGradesDTOS = self.__filterStudents(studentGradesDTOS, discipline)
            if self.__halfPromoted(studentGradesDTOS):
                promotedDisciplines.append(discipline)

        if len(promotedDisciplines) == 0:
            raise NonExistentDisciplineError("Nu exista disipline la care au promovat mai mult de jumatate din studenti!\n")

        return promotedDisciplines

    def getAllGrades(self):
        return self.__gradesRepo.getAllGrades()

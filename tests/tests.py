import data.repositories.catalogue
import domain.student
import domain.discipline
import domain.grade
import validation.errors
import validation.validators
import business.studentService
import business.disciplineService

class Tests:

    def equal(self, list1, list2):
        if len(list1) != len(list2):
            return False
        for i in range(0, len(list1)):
            if list1[i].getID() != list2[i].getID():
                return False
            if list1[i].getFirstName() != list2[i].getFirstName():
                return False
            if list1[i].getLastName() != list2[i].getLastName():
                return False
        return True

    def equalDisciplines(self, list1, list2):
        if len(list1) != len(list2):
            return False
        for i in range(0, len(list1)):
            if list1[i].getID() != list2[i].getID():
                return False
            if list1[i].getName() != list2[i].getName():
                return False
            if list1[i].getTeacherFirst() != list2[i].getTeacherFirst():
                return False
            if list1[i].getTeacherLast() != list2[i].getTeacherLast():
                return False
            if list1[i].getIsOptional() != list2[i].getIsOptional():
                return False
        return True

    def testAddStudent(self):
        catalogue = data.repositories.catalogue.Catalogue()
        student = domain.student.Student("123", "Andrei", "Horvati")
        try:
            catalogue.addStudent(student)
            results = catalogue.getStudents()
            correct = [student]
            assert (self.equal(results, correct))
        except Exception:
            assert(False)

        student3 = domain.student.Student("123", "Raul", "Pele")
        try:
            catalogue.addStudent(student3)
            assert (False)
        except validation.errors.StudentAlreadyExistsError as err:
            assert(str(err) == "Studentul se afla deja in lista!\n")

        student2 = domain.student.Student("1", "Raul", "Pele")
        try:
            catalogue.addStudent(student2)
            results = catalogue.getStudents()
            correct = [student, student2]
            assert(self.equal(results, correct))
        except Exception:
            assert (False)

    def testAddDiscipline(self):
        catalogue = data.repositories.catalogue.Catalogue()
        discipline = domain.discipline.Discipline("1", "Arhitectura sistemelor de calcul", "Alexandru",
                                                  "Vancea", "nu")
        try:
            catalogue.addDiscipline(discipline)
            results = catalogue.getDisciplines()
            correct = [discipline]
            assert(self.equalDisciplines(results, correct))
        except Exception:
            assert (False)

        discipline = domain.discipline.Discipline("1", "Arhitectura sistemelor de calcul", "Alexandru",
                                                  "Vancea", "nu")
        try:
            catalogue.addDiscipline(discipline)
            assert (False)
        except validation.errors.DisciplineAlreadyExistsError as err:
            assert (str(err) == "Disciplina exista deja in facultate!\n")

        discipline2 = domain.discipline.Discipline("2", "Logica Computationala", "A"
                                                  "B", "nu")
        try:
            catalogue.addDiscipline(discipline2)
            results = catalogue.getDisciplines()
            correct = [discipline, discipline2]
            assert (self.equalDisciplines(results, correct))
        except Exception:
            assert (False)

    def testRemoveStudentByID(self):
        catalogue = data.repositories.catalogue.Catalogue()
        student = domain.student.Student("123", "Andrei", "Horvati")
        catalogue.addStudent(student)
        student2 = domain.student.Student("1", "Andrei", "Andrei")
        catalogue.addStudent(student2)

        try:
            catalogue.removeStudentByID("1")
            results = catalogue.getStudents()
            correct = [student]
            assert (self.equal(results, correct))
        except Exception:
            assert False

        try:
            catalogue.removeStudentByID("100")
            assert (False)
        except validation.errors.NonExistentStudentError as err:
            assert (str(err) == "Studentul cu ID-ul dat nu se afla in lista!\n")

    def testRemoveDisciplineByID(self):
        catalogue = data.repositories.catalogue.Catalogue()
        discipline = domain.discipline.Discipline("1", "Arhitectura sistemelor de calcul", "Alexandru",
                                                  "Vancea", "nu")
        catalogue.addDiscipline(discipline)
        discipline2 = domain.discipline.Discipline("2", "Logica Computationala", "a", "b", "da")
        catalogue.addDiscipline(discipline2)

        try:
            catalogue.removeDisciplineByID("1")
            results = catalogue.getDisciplines()
            correct = [discipline2]
            assert (self.equalDisciplines(results, correct))
        except Exception:
            assert False

        try:
            catalogue.removeDisciplineByID("1123")
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err) == "Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n"

    def testAssignGrade(self):
        catalogue = data.repositories.catalogue.Catalogue()
        discipline = domain.discipline.Discipline("1", "Arhitectura sistemelor de calcul", "Alexandru",
                                                  "Vancea", "nu")
        catalogue.addDiscipline(discipline)
        discipline2 = domain.discipline.Discipline("2", "Logica Computationala", "a", "b", "da")
        catalogue.addDiscipline(discipline2)

        student = domain.student.Student("123", "Andrei", "Horvati")

        student2 = domain.student.Student("1", "Andrei", "Andrei")
        catalogue.addStudent(student2)

        try:
            catalogue.assignGrade(domain.grade.Grade(10, "1", "1"))
            assert(student2.getGrades(discipline) == [domain.grade.Grade(10, "1", "1")])
        except Exception as err:
            assert False

        try:
            catalogue.assignGrade(domain.grade.Grade(10, "123123", "1"))
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err) == "Studentul cu ID-ul dat nu se afla in lista studentilor!\n"

        try:
            catalogue.assignGrade(domain.grade.Grade(10, "1", "12312"))
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err) == "Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n"

    def testFindStudentByID(self):
        catalogue = data.repositories.catalogue.Catalogue()
        catalogue.addStudent(domain.student.Student("1", "Raul", "Pele"))
        catalogue.addStudent(domain.student.Student("2", "Andrei", "Andrei"))

        try:
            student = catalogue.findStudentByID("2")
            assert student.getID() == "2"
            assert student.getFirstName() =="Andrei"
            assert student.getLastName() == "Andrei"
        except Exception:
            assert False

        try:
            student = catalogue.findStudentByID("12312")
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err) == "Studentul cu ID-ul dat nu se afla in lista studentilor!\n"

    def testFindDisciplineByID(self):
        catalogue = data.repositories.catalogue.Catalogue()
        discipline = domain.discipline.Discipline("1", "Arhitectura sistemelor de calcul", "Alexandru",
                                                  "Vancea", "nu")
        catalogue.addDiscipline(discipline)

        try:
            discipline = catalogue.findDisciplineByID("123")
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err) == "Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n"

        try:
            discipline = catalogue.findDisciplineByID("1")
            assert discipline.getID() == "1"
            assert discipline.getName() == "Arhitectura Sistemelor De Calcul"
            assert discipline.getTeacherFirst() == "Alexandru"
            assert discipline.getTeacherLast() == "Vancea"
            assert discipline.getIsOptional() == False
        except Exception:
            assert False

    def testAddStudentSrv(self):
        validator = validation.validators.StudentValidator()
        catalogue = data.repositories.catalogue.Catalogue()
        studentSrv = business.studentService.StudentService(catalogue, validator)

        try:
            studentSrv.addStudent("1", "Raul", "Pele")
            student = catalogue.findStudentByID("1")
            assert(student.getID()=="1")
            assert(student.getFirstName() == "Raul")
            assert (student.getLastName() == "Pele")
        except Exception:
            assert False

        try:
            studentSrv.addStudent("1", "Andrei", "Alex")
        except validation.errors.StudentAlreadyExistsError as err:
            assert str(err)=="Studentul se afla deja in lista!\n"

        try:
            studentSrv.addStudent("", "", "")
        except validation.errors.InvalidStudentError as err:
            errors = "ID-ul studentului este invalid!\n"+"Prenumele studentului este invalid!\n"+"Numele studentului este invalid!\n"
            assert str(err)==errors

    def testAddDisciplineSrv(self):
        validator = validation.validators.DisciplineValidator()
        catalogue = data.repositories.catalogue.Catalogue()
        disciplineSrv = business.disciplineService.DisciplineService(catalogue, validator)

        try:
            disciplineSrv.addDiscipline("1", "ASC", "A", "B", "nu")
            discipline = catalogue.findDisciplineByID("1")
            assert(discipline.getID() =="1")
            assert(discipline.getName()=="Asc")
            assert(discipline.getTeacherFirst() == "A")
            assert(discipline.getTeacherLast() == "B")
            assert(discipline.getIsOptional() == False)
        except Exception:
            assert False

        try:
            disciplineSrv.addDiscipline("ab", "123", "Alexandru", "rrqwe13", "fei")
            assert False
        except validation.errors.InvalidDisciplineError as err:
            assert str(err) == "ID-ul disciplinei este invalid!\n" +\
                                "Numele disciplinei este invalid!\n" +\
                                "Numele profesorului este invalid!\n" +\
                                "Nu a fost specificat caracterul disciplinei (optional sau obligatoriu)!\n"

    def testRemoveStudentSrv(self):
        validator = validation.validators.StudentValidator()
        catalogue = data.repositories.catalogue.Catalogue()
        studentSrv = business.studentService.StudentService(catalogue, validator)

        try:
            studentSrv.removeStudent("1aj3")
            assert False
        except validation.errors.InvalidStudentError as err:
            assert str(err) == "Numele sau ID-ul studentului este invalid!\n"

        try:
            studentSrv.removeStudent("1")
            assert False
        except validation.errors.NonExistentStudentError as err:
            assert str(err) == "Studentul cu ID-ul dat nu se afla in lista!\n"

        catalogue.addStudent(domain.student.Student("1", "Raul", "Pele"))
        try:
            studentSrv.removeStudent("1")
            assert True
        except Exception:
            assert False

        catalogue.addStudent(domain.student.Student("1", "Raul", "Pele"))
        try:
            studentSrv.removeStudent("Raul Pele")
            assert True
        except Exception:
            assert False

        try:
            studentSrv.removeStudent("Raul")
        except validation.errors.InvalidStudentError as err:
            assert str(err) == "Numele sau ID-ul studentului este invalid!\n"

    def testRemoveDisciplineSrv(self):
        validator = validation.validators.DisciplineValidator()
        catalogue = data.repositories.catalogue.Catalogue()
        disciplineSrv = business.disciplineService.DisciplineService(catalogue, validator)

        try:
            disciplineSrv.removeDiscipline("aseqw")
            assert False
        except validation.errors.InvalidIDError as err:
            assert str(err)=="ID-ul disciplinei este invalid!\n"

        try:
            disciplineSrv.removeDiscipline("1")
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err) == "Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n"

        catalogue.addDiscipline(domain.discipline.Discipline("1", "asc", "a", "b"))
        try:
            disciplineSrv.removeDiscipline("1")
            assert True
        except Exception:
            assert False

    def testFindStudentSrv(self):
        validator = validation.validators.StudentValidator()
        catalogue = data.repositories.catalogue.Catalogue()
        studentSrv = business.studentService.StudentService(catalogue, validator)

        catalogue.addStudent(domain.student.Student("1", "Raul", "Pele"))

        try:
            student = studentSrv.findStudent("2")
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err) == "Studentul cu ID-ul dat nu se afla in lista studentilor!\n"

        try:
            student = studentSrv.findStudent("1")
            assert student.getID() == "1"
            assert student.getFirstName() == "Raul"
            assert student.getLastName() == "Pele"
        except Exception:
            assert False


    def runTests(self):
        self.testAddStudent()
        self.testAddDiscipline()
        self.testRemoveStudentByID()
        self.testRemoveDisciplineByID()
        self.testAssignGrade()
        self.testAddStudentSrv()
        self.testAddDisciplineSrv()
        self.testRemoveStudentSrv()
        self.testRemoveDisciplineSrv()
        self.testFindStudentSrv()
        self.testFindStudentByID()
        self.testFindDisciplineByID()

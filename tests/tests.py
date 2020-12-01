import data.repositories.catalogue
import data.repositories.GradesRepository
import data.DTOs.StudentPrintDTO
import data.DTOs.StudentGradesDTO
import data.DTOs.StudentGeneralDTO
import domain.student
import domain.discipline
import domain.grade
import validation.errors
import validation.validators
import business.studentService
import business.disciplineService
import business.gradeService
import unittest



class TestCaseStudentService(unittest.TestCase):
    def setUp(self):
        catalogue = data.repositories.catalogue.Catalogue()
        validator = validation.validators.StudentValidator()
        self.studentSrv = business.studentService.StudentService(catalogue, validator)

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

    def testAddStudentSrv(self):
        student1 = domain.student.Student("1", "Raul", "Pele")
        student2 = domain.student.Student("2", "A", "A")

        self.studentSrv.addStudent("1", "Raul", "Pele")
        self.studentSrv.addStudent("2", "A", "A")

        self.assertTrue(self.equal([student2, student1], self.studentSrv.getStudents()))
        self.assertRaises(validation.errors.StudentAlreadyExistsError, self.studentSrv.addStudent,"1", "alex", "alex")
        self.assertRaises(validation.errors.InvalidStudentError, self.studentSrv.addStudent, "", "", "")
        self.assertRaises(validation.errors.InvalidStudentError, self.studentSrv.addStudent, "asewqe", "dasd", "asda")

    def testRemoveStudentSrv(self):
        student1 = domain.student.Student("1", "Raul", "Pele")
        self.studentSrv.addStudent("1", "Raul", "Pele")
        self.studentSrv.addStudent("2", "A", "A")

        self.assertRaises(validation.errors.InvalidStudentError, self.studentSrv.removeStudent, "1aj3")
        self.assertRaises(validation.errors.NonExistentStudentError, self.studentSrv.removeStudent, "3")
        self.studentSrv.removeStudent("2")
        self.assertTrue(self.equal([student1], self.studentSrv.getStudents()))

        self.studentSrv.addStudent("2", "Raul", "Pele")
        self.studentSrv.removeStudent("Raul Pele")
        self.assertEqual(len(self.studentSrv.getStudents()), 0)

    def testFindStudentSrv(self):
        student1 = domain.student.Student("1", "Raul", "Pele")
        student2 = domain.student.Student("2", "A", "A")
        student3 = domain.student.Student("3", "A", "A")

        self.studentSrv.addStudent("1", "Raul", "Pele")
        self.studentSrv.addStudent("2", "A", "A")
        self.studentSrv.addStudent("3", "A", "A")

        self.assertRaises(validation.errors.NonExistentStudentError, self.studentSrv.findStudent, "4")
        results = self.studentSrv.findStudent("1")
        self.assertEqual(results.getID(), "1")
        self.assertEqual(results.getFirstName(), "Raul")
        self.assertEqual(results.getLastName(), "Pele")

        results = self.studentSrv.findStudent("A A")
        self.assertTrue(self.equal(results, [student2, student3]))

        self.assertRaises(validation.errors.InvalidStudentError, self.studentSrv.findStudent, "Raul")

    def testFindStudentByIDSrv(self):
        student1 = domain.student.Student("1", "Raul", "Pele")
        self.studentSrv.addStudent("1", "Raul", "Pele")
        result = self.studentSrv.findStudentByID("1")
        self.assertEqual(result.getID(), "1")
        self.assertEqual(result.getName(), student1.getName())

        self.assertRaises(validation.errors.NonExistentIDError, self.studentSrv.findStudentByID, "399")
        self.assertRaises(validation.errors.InvalidIDError, self.studentSrv.findStudentByID, "1ase321")

    def testFindStudentByNameSrv(self):
        student1 = domain.student.Student("1", "Raul", "Pele")
        student2 = domain.student.Student("2", "A", "A")
        student3 = domain.student.Student("3", "A", "A")
        self.studentSrv.addStudent("1", "Raul", "Pele")
        self.studentSrv.addStudent("2", "A", "A")
        self.studentSrv.addStudent("3", "A", "A")

        self.assertRaises(validation.errors.InvalidNameError, self.studentSrv.findStudentByName,"123sae ewq231")
        self.assertRaises(validation.errors.NonExistentStudentError, self.studentSrv.findStudentByName, "andrei horvati")
        results = self.studentSrv.findStudentByName("A A")
        self.assertTrue(self.equal(results, [student2, student3]))

    def testModifyStudentIDSrv(self):
        student1 = domain.student.Student("123", "a", "b")
        self.studentSrv.addStudent("123", "a", "b")
        self.studentSrv.modifyID("123", "1")
        student2 = self.studentSrv.findStudentByID("1")
        self.assertEqual(student2.getID(), "1")
        self.assertEqual(student2.getFirstName(), "A")
        self.assertEqual(student2.getLastName(), "B")

        self.assertRaises(validation.errors.NonExistentIDError, self.studentSrv.modifyID, "122", "500")
        self.assertRaises(validation.errors.InvalidIDError, self.studentSrv.modifyID,"122", "123deqw3")

    def testModifyStudentNameSrv(self):
        student1 = domain.student.Student("123", "a", "b")
        self.studentSrv.addStudent("123", "a", "b")
        self.studentSrv.modifyName("123", "Raul", "Pele")
        student2 = self.studentSrv.findStudentByID("123")

        self.assertEqual(student2.getFirstName(), "Raul")
        self.assertEqual(student2.getLastName(), "Pele")
        self.assertRaises(validation.errors.NonExistentIDError, self.studentSrv.modifyName, "1", "a", "b")
        self.assertRaises(validation.errors.InvalidNameError, self.studentSrv.modifyName, "123", "312as", "23asde")

class TestCaseDisciplineService(unittest.TestCase):
    def setUp(self):
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()
        validator = validation.validators.DisciplineValidator()

        self.disciplineSrv = business.disciplineService.DisciplineService(catalogue, gradeRepo, validator)

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

    def testAddDisciplineSrv(self):
        discipline1 = domain.discipline.Discipline("1", "ASC", "A", "B", "nu")
        discipline2 = domain.discipline.Discipline("2", "AC", "E", "f", "da")

        self.disciplineSrv.addDiscipline("1", "ASC", "A", "B", "nu")
        self.assertTrue(self.equalDisciplines(self.disciplineSrv.getDisciplines(), [discipline1]))

        self.assertRaises(validation.errors.InvalidDisciplineError, self.disciplineSrv.addDiscipline, "ab", "123", "Alexandru", "rrqwe213", "fei")
        self.assertRaises(validation.errors.DisciplineAlreadyExistsError, self.disciplineSrv.addDiscipline, "1", "A", "B", "C", "da")
        self.assertRaises(validation.errors.DisciplineAlreadyExistsError, self.disciplineSrv.addDiscipline, "3", "ASC", "A", "B", "nu")
        self.disciplineSrv.addDiscipline("2", "AC", "E", "F", "da")
        self.assertTrue(self.equalDisciplines(self.disciplineSrv.getDisciplines(), [discipline2, discipline1]))

    def testRemoveDisciplineSrv(self):
        discipline1 = domain.discipline.Discipline("1", "ASC", "A", "B", "nu")
        discipline2 = domain.discipline.Discipline("2", "ASC", "E", "f", "da")
        discipline3 = domain.discipline.Discipline("3", "Logia computationala", "a", "b", "nu")
        self.disciplineSrv.addDiscipline("1", "ASC", "A", "B", "nu")
        self.disciplineSrv.addDiscipline("2", "ASC", "E", "f", "da")
        self.disciplineSrv.addDiscipline("3", "Logia computationala", "a", "b", "nu")

        self.assertRaises(validation.errors.NonExistentDisciplineError, self.disciplineSrv.removeDiscipline, "Aasdaewq")
        self.assertRaises(validation.errors.NonExistentDisciplineError, self.disciplineSrv.removeDiscipline, "599")
        self.assertRaises(validation.errors.InvalidDisciplineError, self.disciplineSrv.removeDiscipline, "1EQS")
        self.disciplineSrv.removeDiscipline("3")
        self.assertTrue(self.equalDisciplines(self.disciplineSrv.getDisciplines(), [discipline1, discipline2]))
        self.disciplineSrv.removeDiscipline("ASC")
        self.assertEqual(len(self.disciplineSrv.getDisciplines()), 0)

    def testModifyDiscIDSrv(self):
        self.disciplineSrv.addDiscipline("100", "ASC", "A", "B", "NU")
        self.disciplineSrv.modifyID("100", "1")
        self.assertEqual(self.disciplineSrv.getDisciplines()[0].getID(), "1")

        self.assertRaises(validation.errors.NonExistentIDError, self.disciplineSrv.modifyID, "1asdw3123", "3")
        self.assertRaises(validation.errors.InvalidIDError, self.disciplineSrv.modifyID, "1", "1sad21312se")

    def testModifyDiscNameSrv(self):
        self.disciplineSrv.addDiscipline("1", "ASC", "A", "B", "NU")
        self.disciplineSrv.modifyDiscName("1", "Arhitectura sistemelor de calcul")
        self.assertEqual(self.disciplineSrv.getDisciplines()[0].getName(), "Arhitectura Sistemelor De Calcul")
        self.assertRaises(validation.errors.InvalidNameError, self.disciplineSrv.modifyDiscName, "1", "123")
        self.assertRaises(validation.errors.NonExistentIDError, self.disciplineSrv.modifyDiscName, "12awe3", "A")

    def testModifyTeacherSrv(self):
        self.disciplineSrv.addDiscipline("1", "ASC", "A", "B", "NU")
        self.assertRaises(validation.errors.InvalidNameError, self.disciplineSrv.modifyTeacher, "1", "Alexandru", "21312EASE")
        self.assertRaises(validation.errors.NonExistentIDError, self.disciplineSrv.modifyTeacher, "123123", "Alexandru", "Vancea")
        self.disciplineSrv.modifyTeacher("1", "Alexandru", "Vancea")
        self.assertEqual(self.disciplineSrv.getDisciplines()[0].getTeacher(), "Alexandru Vancea")

    def testModifyDiscOptionalSrv(self):
        self.disciplineSrv.addDiscipline("1", "ASC", "A", "B", "NU")
        self.assertRaises(validation.errors.NonExistentIDError,self.disciplineSrv.modifyOptional, "1000", True)
        self.disciplineSrv.modifyOptional("1", True)
        self.assertEqual(self.disciplineSrv.findDiscipline("1").getIsOptional(), True)

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

    def testAddGradeSrv(self):
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()
        discValidator = validation.validators.DisciplineValidator()
        studValidator = validation.validators.StudentValidator()
        gradeValidator = validation.validators.GradeValidator()
        gradeSrv = business.gradeService.GradeService(gradeRepo, catalogue, discValidator, studValidator, gradeValidator)
        student = domain.student.Student("1", "Raul", "Pele")

        discipline = domain.discipline.Discipline("1", "asc", "a", "b", "nu")
        catalogue.addStudent(student)
        catalogue.addDiscipline(discipline)
        grade1 = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(5, "1", "1")
        grade3 = domain.grade.Grade(5, "1", "2")

        try:
            gradeSrv.addGrade("1", "1", 10)
            gradeSrv.addGrade("1", "1", 5)
            assert gradeRepo.getAllGrades() == [grade1, grade2]
        except Exception:
            assert False

        try:
            gradeSrv.addGrade("1", "2", 5)
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err) == "Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n"

        try:
            gradeSrv.addGrade("1", "asodsifj3123", 10)
            assert False
        except validation.errors.InvalidIDError as err:
            assert str(err) == "ID-ul disciplinei este invalid!\n"

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

    def testAssignGradeSrv(self):
        catalogue = data.repositories.catalogue.Catalogue()
        discValidator = validation.validators.DisciplineValidator()
        studValidator = validation.validators.StudentValidator()
        gradeValidator = validation.validators.GradeValidator()
        gradeSrv = business.gradeService.GradeService(catalogue, discValidator, studValidator, gradeValidator)

        discipline = domain.discipline.Discipline("1", "asc", "a", "b", "nu")
        student = domain.student.Student("1", "Raul", "Pele")
        catalogue.addStudent(student)
        catalogue.addDiscipline(discipline)

        try:
            grade = domain.grade.Grade(10, "1", "1")
            gradeSrv.assignGrade("1", "1", 10)
            assert student.getGrades(discipline) == [grade]
        except Exception:
            assert False

        try:
            grade = domain.grade.Grade(-2, "1A", "132")
            gradeSrv.assignGrade("1", "1", 10)
            assert student.getGrades(discipline) == [grade]
        except Exception:
            assert False

    def testRemoveStudentByName(self):
        validator = validation.validators.StudentValidator()
        catalogue = data.repositories.catalogue.Catalogue()
        studentSrv = business.studentService.StudentService(catalogue, validator)

        catalogue.addStudent(domain.student.Student("1", "Raul", "Pele"))
        catalogue.addStudent(domain.student.Student("2", "Raul", "Pele"))

        try:
            catalogue.removeStudentByName("Andrei H")
            assert False
        except validation.errors.NonExistentStudentError as err:
            assert str(err)=="Studentul cu numele dat nu se afla in lista!\n"

        try:
            catalogue.removeStudentByName("Raul Pele")
            assert catalogue.getStudents() == []
        except Exception:
            assert False

    def testRemoveDisciplineByName(self):
        validator = validation.validators.DisciplineValidator()
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()
        disciplineSrv = business.disciplineService.DisciplineService(catalogue, gradeRepo, validator)

        discipline1 = domain.discipline.Discipline("1", "Asc", "A", "V", "nu")
        discipline2 = domain.discipline.Discipline("2", "Asc", "B", "C")
        discipline3 = domain.discipline.Discipline("3", "Lc", "B", "C")
        disciplineSrv.addDiscipline(discipline1.getID(), discipline1.getName(), discipline1.getTeacherFirst(), discipline1.getTeacherLast(), "nu")
        disciplineSrv.addDiscipline(discipline2.getID(), discipline2.getName(), discipline2.getTeacherFirst(), discipline2.getTeacherLast(), "da")
        disciplineSrv.addDiscipline(discipline3.getID(), discipline3.getName(), discipline3.getTeacherFirst(), discipline3.getTeacherLast(), "da")

        try:
            catalogue.removeDisciplineByName("asc")
            results = catalogue.getDisciplines()
            correct = [discipline3]
            assert self.equalDisciplines(results, correct)
        except Exception:
            assert False

        try:
            catalogue.removeDisciplineByName("asc")
            assert False
        except validation.errors.NonExistentDisciplineError as err:
            assert str(err) == "Disciplina cu numele dat nu se afla in lista!\n"

    def testSelectOptionalsByID(self):
        validator = validation.validators.DisciplineValidator()
        catalogue = data.repositories.catalogue.Catalogue()

        student = domain.student.Student("1", "Raul", "Pele")
        discipline1 = domain.discipline.Discipline("1", "Asc", "A", "V", "nu")
        discipline2 = domain.discipline.Discipline("2", "Asc", "B", "C")
        discipline3 = domain.discipline.Discipline("3", "Lc", "B", "C")

        catalogue.addStudent(student)
        catalogue.addDiscipline(discipline1)
        catalogue.addDiscipline(discipline2)
        catalogue.addDiscipline(discipline3)

        try:
            catalogue.selectOptionalsByID("1", "2")
            assert self.equalDisciplines(student.getOptionals(), [discipline2])
        except Exception:
            assert False

        try:
            catalogue.selectOptionalsByID("1", "asfieo")
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err)=="Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n"


    def testRemoveOptionalsByID(self):
        validator = validation.validators.DisciplineValidator()
        catalogue = data.repositories.catalogue.Catalogue()

        student = domain.student.Student("1", "Raul", "Pele")
        discipline1 = domain.discipline.Discipline("1", "Asc", "A", "V", "nu")
        discipline2 = domain.discipline.Discipline("2", "Asc", "B", "C")
        discipline3 = domain.discipline.Discipline("3", "Lc", "B", "C")
        catalogue.addStudent(student)
        catalogue.addDiscipline(discipline1)
        catalogue.addDiscipline(discipline2)
        catalogue.addDiscipline(discipline3)
        catalogue.selectOptionalsByID("1", "2")
        catalogue.selectOptionalsByID("1", "3")

        try:
            catalogue.removeOptionalsByID("1", "123")
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err) == "Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n"

        try:
            catalogue.removeOptionalsByID("1", "2")
            assert True
        except Exception:
            assert False

    def testModifyDiscID(self):
        catalogue = data.repositories.catalogue.Catalogue()
        discipline1 = domain.discipline.Discipline("1", "Asc", "A", "V", "nu")
        catalogue.addDiscipline(discipline1)

        catalogue.modifyDiscID(discipline1, "2")
        assert discipline1.getID() == "2"

    def testModifyDiscName(self):
        catalogue = data.repositories.catalogue.Catalogue()
        discipline1 = domain.discipline.Discipline("1", "Asc", "A", "V", "nu")
        catalogue.addDiscipline(discipline1)

        catalogue.modifyDiscName(discipline1, "arhitectura sistemelor de calcul")
        assert discipline1.getName() == "Arhitectura Sistemelor De Calcul"

    def testModifyTeacher(self):
        catalogue = data.repositories.catalogue.Catalogue()
        discipline1 = domain.discipline.Discipline("1", "Asc", "A", "V", "nu")
        catalogue.addDiscipline(discipline1)

        catalogue.modifyDiscTeacher(discipline1, "Alexandru", "Vancea")
        assert discipline1.getTeacher() == "Alexandru Vancea"

    def testModifyOptional(self):
        catalogue = data.repositories.catalogue.Catalogue()
        discipline1 = domain.discipline.Discipline("1", "Asc", "A", "V", "nu")
        catalogue.addDiscipline(discipline1)

        catalogue.modifyDiscOptional(discipline1, True)
        assert discipline1.getIsOptional() == True

    def testGetStudentInfoByIDSrv(self):
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()
        studValidator = validation.validators.StudentValidator()
        discValidator = validation.validators.DisciplineValidator()
        gradeValidator = validation.validators.GradeValidator()

        gradeSrv = business.gradeService.GradeService(gradeRepo, catalogue, discValidator, studValidator, gradeValidator)

        student = domain.student.Student("1", "Raul", "Pele")
        discipline = domain.discipline.Discipline("1", "asc", "a", "b", "nu")
        grade = domain.grade.Grade(10, "1", "1")
        catalogue.addStudent(student)
        catalogue.addDiscipline(discipline)
        gradeSrv.addGrade("1", "1", 10)

        try:
            results = gradeSrv.getStudentInfoByID("1")
            correct = data.DTOs.StudentPrintDTO.StudentPrintDTO(student, [discipline], [grade], 10.0)

            assert str(results) == str(correct)
        except Exception:
            assert False

        try:
            results = gradeSrv.getStudentInfoByID("asijde123")
            assert False
        except validation.validators.InvalidIDError as err:
            assert str(err) == "ID-ul studentului este invalid!\n"

        try:
            results = gradeSrv.getStudentInfoByID("300")
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err) == "Studentul cu ID-ul dat nu se afla in lista studentilor!\n"

    def testGetStudentInfoByNameSrv(self):
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()
        studValidator = validation.validators.StudentValidator()
        discValidator = validation.validators.DisciplineValidator()
        gradeValidator = validation.validators.GradeValidator()

        gradeSrv = business.gradeService.GradeService(gradeRepo, catalogue, discValidator, studValidator,
                                                      gradeValidator)

        student = domain.student.Student("1", "Raul", "Pele")
        student2 = domain.student.Student("2", "Raul", "Pele")
        discipline = domain.discipline.Discipline("1", "asc", "a", "b", "nu")
        grade = domain.grade.Grade(10, "1", "1")
        catalogue.addStudent(student)
        catalogue.addStudent(student2)
        catalogue.addDiscipline(discipline)
        gradeSrv.addGrade("1", "1", 10)

        try:
            results = gradeSrv.getStudentInfoByName("Raul Pele")
            correct1 = data.DTOs.StudentPrintDTO.StudentPrintDTO(student, [discipline], [grade], 10.0)
            correct2 = data.DTOs.StudentPrintDTO.StudentPrintDTO(student2, [discipline], [], 0)
            assert str(results[0]) == str(correct1)

            assert str(results[1]) == str(correct2)
        except Exception:
            assert False

        try:
            results = gradeSrv.getStudentInfoByName("asijde123")
            assert False
        except validation.validators.InvalidNameError as err:
            assert str(err) == "Numele studentului este invalid!\n"

        try:
            results = gradeSrv.getStudentInfoByName("Andrei Alex")
            assert False
        except validation.errors.NonExistentStudentError as err:
            assert str(err) == "Studentul cu numele dat nu se afla in lista!\n"

    def testGetAverage(self):
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()
        studValidator = validation.validators.StudentValidator()
        discValidator = validation.validators.DisciplineValidator()
        gradeValidator = validation.validators.GradeValidator()

        gradeSrv = business.gradeService.GradeService(gradeRepo, catalogue, discValidator, studValidator,
                                                      gradeValidator)
        student = domain.student.Student("1", "Raul", "Pele")

        discipline = domain.discipline.Discipline("1", "asc", "a", "b", "nu")
        catalogue.addStudent(student)
        catalogue.addDiscipline(discipline)
        gradeSrv.addGrade("1", "1", 10)
        gradeSrv.addGrade("1", "1", 5)

        average = gradeRepo.getAverage("1")
        assert average == (10+5)/2

        average = gradeRepo.getAverage("2")
        assert average == 0

    def testGetAllForStudent(self):
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()

        student = domain.student.Student("1", "Raul", "Pele")

        discipline = domain.discipline.Discipline("1", "asc", "a", "b", "nu")
        catalogue.addStudent(student)
        catalogue.addDiscipline(discipline)
        grade1 = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(5, "1", "1")

        gradeRepo.addGrade(grade1)
        gradeRepo.addGrade(grade2)

        grades = gradeRepo.getAllForStudent("1")
        assert grades == [grade1, grade2]

    def testRemoveDisciplineGradesByID(self):
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()

        student = domain.student.Student("1", "Raul", "Pele")

        discipline = domain.discipline.Discipline("1", "asc", "a", "b", "nu")
        catalogue.addStudent(student)
        catalogue.addDiscipline(discipline)
        grade1 = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(5, "1", "1")
        grade3 = domain.grade.Grade(5, "1", "2")

        gradeRepo.addGrade(grade1)
        gradeRepo.addGrade(grade2)
        gradeRepo.addGrade(grade3)

        try:
            gradeRepo.removeDisciplineGradesByID("1")
            assert gradeRepo.getAllGrades() == [grade3]
        except Exception:
            assert False

        try:
            gradeRepo.removeDisciplineGradesByID("1000")
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err) == "Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n"

    def testRemoveGrade(self):
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()

        student = domain.student.Student("1", "Raul", "Pele")

        discipline = domain.discipline.Discipline("1", "asc", "a", "b", "nu")
        catalogue.addStudent(student)
        catalogue.addDiscipline(discipline)
        grade1 = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(5, "1", "1")
        grade3 = domain.grade.Grade(5, "1", "2")

        gradeRepo.addGrade(grade1)
        gradeRepo.addGrade(grade2)
        gradeRepo.addGrade(grade3)

        try:
            gradeRepo.removeGrade(grade1)
            assert gradeRepo.getAllGrades() == [grade2, grade3]
        except Exception:
            assert False

        try:
            gradeRepo.removeGrade(grade1)
            assert False
        except validation.errors.NonExistentGradeError as err:
            assert str(err) == "Nota nu se afla in lista de note!\n"


    def testRemoveGradeSrv(self):
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()
        studValidator = validation.validators.StudentValidator()
        discValidator = validation.validators.DisciplineValidator()
        gradeValidator = validation.validators.GradeValidator()

        gradeSrv = business.gradeService.GradeService(gradeRepo, catalogue, discValidator, studValidator,
                                                      gradeValidator)
        discipline = domain.discipline.Discipline("1", "a", "b", "c", "nu")
        catalogue.addDiscipline(discipline)
        grade1= domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(10, "1", "1")
        grade3 = domain.grade.Grade(3, "1", "1")
        gradeRepo.addGrade(grade1)
        gradeRepo.addGrade(grade2)
        gradeRepo.addGrade(grade3)


        try:
            gradeSrv.removeGrade("1", "1", 10)
            assert gradeRepo.getAllGrades() == [grade2, grade3]
        except Exception:
            assert False

        try:
            gradeSrv.removeGrade("1", "129312asdsfes", 10)
            assert False
        except validation.errors.InvalidIDError as err:
            assert str(err) == "ID-ul disciplinei este invalid!\n"

        try:
            gradeSrv.removeGrade("1", "1", -123)
            assert False
        except validation.errors.InvalidGradeError as err:
            assert str(err) == "Nota trebuie as fie un numar real intre 1 si 10!\n"

        try:
            gradeSrv.removeGrade("1", "1", 7)
            assert False
        except validation.errors.NonExistentGradeError as err:
            assert str(err) == "Nota nu se afla in lista de note!\n"

    def testGetDisciplineGrades(self):
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()

        discipline = domain.discipline.Discipline("1", "a", "b", "c", "nu")
        catalogue.addDiscipline(discipline)
        grade1 = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(10, "2", "1")
        grade3 = domain.grade.Grade(3, "1", "1")
        grade4 = domain.grade.Grade(5, "1", "2")
        gradeRepo.addGrade(grade1)
        gradeRepo.addGrade(grade2)
        gradeRepo.addGrade(grade3)
        gradeRepo.addGrade(grade4)

        discGrades = gradeRepo.getDisciplineGrades("1", "1")
        assert discGrades == [grade1, grade3]

    def testGetStudentsFromDisciplineSrv(self):
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()
        studValidator = validation.validators.StudentValidator()
        discValidator = validation.validators.DisciplineValidator()
        gradeValidator = validation.validators.GradeValidator()

        gradeSrv = business.gradeService.GradeService(gradeRepo, catalogue, discValidator, studValidator,
                                                      gradeValidator)
        discipline = domain.discipline.Discipline("1", "a", "b", "c", "nu")
        student1 = domain.student.Student("1", "a", "b")
        student2 = domain.student.Student("2", "c", "d")
        catalogue.addDiscipline(discipline)
        grade1 = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(10, "1", "1")
        grade3 = domain.grade.Grade(3, "2", "1")
        gradeRepo.addGrade(grade1)
        gradeRepo.addGrade(grade2)
        gradeRepo.addGrade(grade3)
        catalogue.addStudent(student1)
        catalogue.addStudent(student2)

        student1DTO= data.DTOs.StudentGradesDTO.StudentGradesDTO(student1, [grade1, grade2], 10)
        student2DTO= data.DTOs.StudentGradesDTO.StudentGradesDTO(student2, [grade3], 3)


        try:
            students = gradeSrv.getStudentsFromDiscipline("1")
            assert students == [student1DTO, student2DTO]
        except Exception:
            assert False

        try:
            students = gradeSrv.getStudentsFromDiscipline("ASE123")
            assert False
        except validation.errors.InvalidIDError as err:
            assert str(err) == "ID-ul disciplinei este invalid!\n"

        try:
            students = gradeSrv.getStudentsFromDiscipline("300")
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err) == "Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n"

    def testGetStudentsFromDisciplineSortedByAvgSrv(self):
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()
        studValidator = validation.validators.StudentValidator()
        discValidator = validation.validators.DisciplineValidator()
        gradeValidator = validation.validators.GradeValidator()

        gradeSrv = business.gradeService.GradeService(gradeRepo, catalogue, discValidator, studValidator,
                                                      gradeValidator)
        discipline = domain.discipline.Discipline("1", "a", "b", "c", "nu")
        student1 = domain.student.Student("1", "a", "b")
        student2 = domain.student.Student("2", "c", "d")
        catalogue.addDiscipline(discipline)
        grade1 = domain.grade.Grade(3, "1", "1")
        grade2 = domain.grade.Grade(2, "1", "1")
        grade3 = domain.grade.Grade(10, "2", "1")
        gradeRepo.addGrade(grade1)
        gradeRepo.addGrade(grade2)
        gradeRepo.addGrade(grade3)
        catalogue.addStudent(student1)
        catalogue.addStudent(student2)

        student1DTO= data.DTOs.StudentGradesDTO.StudentGradesDTO(student1, [grade1, grade2], 2.5)
        student2DTO= data.DTOs.StudentGradesDTO.StudentGradesDTO(student2, [grade3], 10)

        try:
            students = gradeSrv.getStudentsFromDisciplineSortedByAvg("1")

            assert students == [student2DTO, student1DTO]
        except Exception:
            assert False

        try:
            students = gradeSrv.getStudentsFromDisciplineSortedByAvg("ASE123")
            assert False
        except validation.errors.InvalidIDError as err:
            assert str(err) == "ID-ul disciplinei este invalid!\n"

        try:
            students = gradeSrv.getStudentsFromDisciplineSortedByAvg("300")
            assert False
        except validation.errors.NonExistentIDError as err:
            assert str(err) == "Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n"

    def testGetTop20PercentSrv(self):
        catalogue = data.repositories.catalogue.Catalogue()
        gradeRepo = data.repositories.GradesRepository.GradesRepository()
        studValidator = validation.validators.StudentValidator()
        discValidator = validation.validators.DisciplineValidator()
        gradeValidator = validation.validators.GradeValidator()

        gradeSrv = business.gradeService.GradeService(gradeRepo, catalogue, discValidator, studValidator,
                                                      gradeValidator)
        discipline = domain.discipline.Discipline("1", "a", "b", "c", "nu")
        student1 = domain.student.Student("1", "a", "b")
        student2 = domain.student.Student("2", "c", "d")
        student3 = domain.student.Student("3", "c", "a")
        student4 = domain.student.Student("4", "d", "a")
        student5 = domain.student.Student("5", "a", "c")
        catalogue.addDiscipline(discipline)
        grade1 = domain.grade.Grade(3, "1", "1")
        grade2 = domain.grade.Grade(2, "1", "1")
        grade3 = domain.grade.Grade(10, "2", "1")
        grade4 = domain.grade.Grade(5, "3", "1")
        grade5 = domain.grade.Grade(4, "5", "1")

        gradeRepo.addGrade(grade1)
        gradeRepo.addGrade(grade2)
        gradeRepo.addGrade(grade3)
        gradeRepo.addGrade(grade4)
        gradeRepo.addGrade(grade5)
        catalogue.addStudent(student1)
        catalogue.addStudent(student2)
        catalogue.addStudent(student3)
        catalogue.addStudent(student4)
        catalogue.addStudent(student5)

        student1DTO = data.DTOs.StudentGeneralDTO.StudentGeneralDTO(student2, 10)

        try:
            students = gradeSrv.getTop20Percent()
            assert students == [student1DTO]
        except Exception:
            assert False

        catalogue.removeStudentByID("4")

        try:
            students = gradeSrv.getTop20Percent()
            assert False
        except validation.errors.NonExistentStudentError as err:
            assert str(err) == "Nu exista suficienti studenti in lista!\n"

    def runTests(self):
        self.testAddStudent()
        self.testAddDiscipline()
        self.testRemoveStudentByID()
        self.testRemoveDisciplineByID()
        self.testAddStudentSrv()
        self.testAddDisciplineSrv()
        self.testRemoveStudentSrv()
        self.testRemoveDisciplineSrv()
        self.testFindStudentSrv()
        self.testFindStudentByID()
        self.testFindDisciplineByID()
        self.testAddGradeSrv()
        self.testRemoveStudentByName()
        self.testRemoveDisciplineByName()
        self.testModifyStudentID()
        self.testModifyStudentName()
        self.testModifyStudentIDSrv()
        self.testModifyStudentNameSrv()
        self.testSelectOptionalsByID()
        self.testRemoveOptionalsByID()
        self.testModifyDiscID()
        self.testModifyDiscName()
        self.testModifyTeacher()
        self.testModifyOptional()
        self.testModifyDiscIDSrv()
        self.testModifyDiscNameSrv()
        self.testModifyTeacherSrv()
        self.testModifyDiscOptionalSrv()
        self.testFindStudentByName()
        self.testGetStudentInfoByIDSrv()
        self.testGetStudentInfoByNameSrv()
        self.testGetAverage()
        self.testGetAllForStudent()
        self.testRemoveDisciplineGradesByID()
        self.testRemoveGrade()
        self.testRemoveGradeSrv()
        self.testGetDisciplineGrades()
        self.testGetStudentsFromDisciplineSrv()
        self.testGetStudentsFromDisciplineSortedByAvgSrv()
        self.testGetTop20PercentSrv()

if __name__ == "__main__":
    unittest.main()
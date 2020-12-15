import data.repositories.catalogue
import data.repositories.catalogueFileRepo
import data.repositories.GradesRepository
import data.repositories.GradesFileRepo
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
import os

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

    def testFindDiciplineSrv(self):
        self.disciplineSrv.addDiscipline("1", "ASC", "A", "B", "NU")
        self.disciplineSrv.addDiscipline("3", "Logia computationala", "a", "b", "nu")
        result = self.disciplineSrv.findDiscipline("1")

        self.assertEqual(result.getID(), "1")
        self.assertEqual(result.getName(), "Asc")
        self.assertEqual(result.getTeacherFirst(), "A")
        self.assertEqual(result.getTeacherLast(), "B")
        self.assertEqual(result.getIsOptional(), False)

        self.assertRaises(validation.errors.InvalidIDError, self.disciplineSrv.findDiscipline, "123asdweq")
        self.assertRaises(validation.errors.NonExistentIDError, self.disciplineSrv.findDiscipline, "300")



class TestCaseGradeService(unittest.TestCase):
    def setUp(self):
        gradesRepo = data.repositories.GradesRepository.GradesRepository()
        self.catalogue = data.repositories.catalogue.Catalogue()
        studValidator = validation.validators.StudentValidator()
        discValidator = validation.validators.DisciplineValidator()
        gradeValidator = validation.validators.GradeValidator()

        self.catalogue.addDiscipline(domain.discipline.Discipline("1", "Arhitectura Sistemelor De Calcul", "Alexandru", "Vancea", "nu"))
        self.catalogue.addDiscipline(domain.discipline.Discipline("2", "Logica Computationala", "A", "B", "nu"))
        self.catalogue.addDiscipline(domain.discipline.Discipline("3", "Arhitectura Sistemelor de Calcul", "A", "E", "da"))
        self.catalogue.addStudent(domain.student.Student("1", "Raul", "Pele"))
        self.catalogue.addStudent(domain.student.Student("2", "Andrei", "H"))

        self.gradeSrv = business.gradeService.GradeService(gradesRepo, self.catalogue, discValidator, studValidator, gradeValidator)

    def testAddGradeSrv(self):
        self.assertRaises(validation.errors.InvalidGradeError, self.gradeSrv.addGrade, "1", "1", -6.5)
        self.assertRaises(validation.errors.InvalidIDError, self.gradeSrv.addGrade, "-12a", "1", 10)
        self.assertRaises(validation.errors.InvalidIDError, self.gradeSrv.addGrade, "1", "-12A", 5.25)
        self.assertRaises(validation.errors.NonExistentIDError, self.gradeSrv.addGrade, "300", "3", 10)
        self.assertRaises(validation.errors.NonExistentIDError, self.gradeSrv.addGrade, "1", "333", 10)
        self.assertRaises(validation.errors.NonExistentIDError, self.gradeSrv.addGrade, "1", "3", 5.55)
        grade1 = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(7.5, "1", "2")
        self.gradeSrv.addGrade("1", "1", 10)
        self.gradeSrv.addGrade("1", "2", 7.5)
        self.assertEqual(self.gradeSrv.getAllGrades(), [grade1, grade2])

    def testRemoveGradeSrv(self):
        grade1 = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(7.5, "1", "2")
        self.gradeSrv.addGrade("1", "1", 10)
        self.gradeSrv.addGrade("1", "2", 7.5)

        self.gradeSrv.removeGrade("1", "2", 7.5)
        self.assertEqual(self.gradeSrv.getAllGrades(), [grade1])
        self.assertRaises(validation.errors.InvalidIDError, self.gradeSrv.removeGrade, "1ASDWEQ", "1", 10)
        self.assertRaises(validation.errors.InvalidIDError, self.gradeSrv.removeGrade, "1", "1ASEWE3213", 10)
        self.assertRaises(validation.errors.NonExistentIDError, self.gradeSrv.removeGrade, "100", "1", 10)
        self.assertRaises(validation.errors.NonExistentIDError, self.gradeSrv.removeGrade, "1", "100", 10)
        self.assertRaises(validation.errors.NonExistentGradeError, self.gradeSrv.removeGrade, "1", "1", 6.54)

    def testGetStudentInfoByIDSrv(self):
        grade1 = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(7.5, "1", "2")
        self.gradeSrv.addGrade("1", "1", 10)
        self.gradeSrv.addGrade("1", "2", 7.5)
        student1 = self.catalogue.findStudentByID("1")
        dto1 = data.DTOs.StudentPrintDTO.StudentPrintDTO(student1, student1.getDisciplines(), [grade1, grade2], (10+7.5)/2)
        self.assertEqual(str(dto1), str(self.gradeSrv.getStudentInfoByID("1")))
        self.assertRaises(validation.errors.InvalidIDError, self.gradeSrv.getStudentInfoByID, "123asdwqeqw")
        self.assertRaises(validation.errors.NonExistentIDError, self.gradeSrv.getStudentInfoByID, "300")

    def testGetStudentInfoByNameSrv(self):
        student = self.catalogue.findStudentByID("1")
        student2 = domain.student.Student("3", "Raul", "Pele")
        self.catalogue.addStudent(student2)
        grade = domain.grade.Grade(10, "1", "1")
        self.gradeSrv.addGrade("1", "1", 10)
        correct1 = data.DTOs.StudentPrintDTO.StudentPrintDTO(student, student.getDisciplines(), [grade], 10.0)
        correct2 = data.DTOs.StudentPrintDTO.StudentPrintDTO(student2, student2.getDisciplines(), [], 0)
        results = self.gradeSrv.getStudentInfoByName("Raul Pele")
        self.assertEqual(str(correct1), str(results[0]))
        self.assertEqual(str(correct2), str(results[1]))
        self.assertRaises(validation.errors.InvalidNameError, self.gradeSrv.getStudentInfoByName, "123asdqwesa")
        self.assertRaises(validation.errors.NonExistentStudentError, self.gradeSrv.getStudentInfoByName, "Andrei Alex")

    def testGetStudentsFromDisciplineSrv(self):
        grade1 = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(7.5, "1", "1")
        grade3 = domain.grade.Grade(10, "2", "1")
        self.gradeSrv.addGrade("1", "1", 10)
        self.gradeSrv.addGrade("1", "1", 7.5)
        self.gradeSrv.addGrade("2", "1", 10)
        student1 = self.catalogue.findStudentByID("1")
        student2=self.catalogue.findStudentByID("2")

        student1DTO = data.DTOs.StudentGradesDTO.StudentGradesDTO(student1, [grade1, grade2], (10+7.5)/2)
        student2DTO = data.DTOs.StudentGradesDTO.StudentGradesDTO(student2, [grade3], 10)
        self.assertEqual(self.gradeSrv.getStudentsFromDiscipline("1"), [student2DTO, student1DTO])

        self.assertRaises(validation.errors.InvalidIDError, self.gradeSrv.getStudentsFromDiscipline, "1asdweq32")
        self.assertRaises(validation.errors.NonExistentIDError, self.gradeSrv.getStudentsFromDiscipline, "100")
        self.assertRaises(validation.errors.NonExistentStudentError, self.gradeSrv.getStudentsFromDiscipline, "3")

    def testGetStudentsFromDisciplineSortedByAvgSrv(self):
        grade1 = domain.grade.Grade(3, "1", "1")
        grade2 = domain.grade.Grade(2, "1", "1")
        grade3 = domain.grade.Grade(10, "2", "1")
        self.gradeSrv.addGrade("1", "1", 3)
        self.gradeSrv.addGrade("1", "1", 2)
        self.gradeSrv.addGrade("2", "1", 10)
        student1 = self.catalogue.findStudentByID("1")
        student2 = self.catalogue.findStudentByID("2")
        student1DTO = data.DTOs.StudentGradesDTO.StudentGradesDTO(student1, [grade1, grade2], 2.5)
        student2DTO = data.DTOs.StudentGradesDTO.StudentGradesDTO(student2, [grade3], 10)

        self.assertEqual(self.gradeSrv.getStudentsFromDisciplineSortedByAvg("1"), [student2DTO, student1DTO])

    def testGetTop20Percent(self):
        student2 = self.catalogue.findStudentByID("2")
        student3 = domain.student.Student("3", "c", "a")
        student4 = domain.student.Student("4", "d", "a")
        student5 = domain.student.Student("5", "a", "c")

        self.catalogue.addStudent(student3)
        self.catalogue.addStudent(student4)
        self.catalogue.addStudent(student5)
        self.gradeSrv.addGrade("1", "1", 3)
        self.gradeSrv.addGrade("1", "1", 2)
        self.gradeSrv.addGrade("2", "1", 10)
        self.gradeSrv.addGrade("3", "1", 5)
        self.gradeSrv.addGrade("5", "1", 4)
        student1DTO = data.DTOs.StudentGeneralDTO.StudentGeneralDTO(student2, 10)

        self.assertEqual(self.gradeSrv.getTop20Percent(), [student1DTO])
        self.catalogue.removeStudentByID("4")
        self.assertRaises(validation.errors.NonExistentStudentError, self.gradeSrv.getTop20Percent)


class TestCaseCatalogue(unittest.TestCase):
    def setUp(self):
        self.catalogue = data.repositories.catalogue.Catalogue()

    def testSelectOptionalsByID(self):
        student = domain.student.Student("1", "Raul", "Pele")
        discipline1 = domain.discipline.Discipline("1", "Asc", "A", "V", "nu")
        discipline2 = domain.discipline.Discipline("2", "Asc", "B", "C")
        discipline3 = domain.discipline.Discipline("3", "Lc", "B", "C")

        self.catalogue.addStudent(student)
        self.catalogue.addDiscipline(discipline1)
        self.catalogue.addDiscipline(discipline2)
        self.catalogue.addDiscipline(discipline3)

        self.catalogue.selectOptionalsByID("1", "2")
        self.assertEqual(student.getOptionals(), [discipline2])
        self.assertRaises(validation.errors.NonExistentIDError, self.catalogue.selectOptionalsByID, "1", "asdqwesad")

    def testRemoveOptionalsByID(self):
        student = domain.student.Student("1", "Raul", "Pele")
        discipline1 = domain.discipline.Discipline("1", "Asc", "A", "V", "nu")
        discipline2 = domain.discipline.Discipline("2", "Asc", "B", "C")
        discipline3 = domain.discipline.Discipline("3", "Lc", "B", "C")

        self.catalogue.addStudent(student)
        self.catalogue.addDiscipline(discipline1)
        self.catalogue.addDiscipline(discipline2)
        self.catalogue.addDiscipline(discipline3)
        self.catalogue.selectOptionalsByID("1", "2")
        self.catalogue.selectOptionalsByID("1", "3")

        self.assertRaises(validation.errors.NonExistentIDError, self.catalogue.removeOptionalsByID, "1", "123")
        self.catalogue.removeOptionalsByID("1", "2")
        self.assertEqual(student.getOptionals(), [discipline3])


class TestCaseGradesRepository(unittest.TestCase):
    def setUp(self):
        self.gradesRepo = data.repositories.GradesRepository.GradesRepository()

    def testGetAverage(self):
        self.gradesRepo.addGrade(domain.grade.Grade(10, "1", "1"))
        self.gradesRepo.addGrade(domain.grade.Grade(5, "1", "1"))
        self.assertEqual(self.gradesRepo.getAverage("1"), (10+5)/2)
        self.assertEqual(self.gradesRepo.getAverage("2"), 0)

    def testGetAllForStudent(self):
        grade1 = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(5, "1", "1")
        self.gradesRepo.addGrade(grade1)
        self.gradesRepo.addGrade(grade2)

        self.assertEqual(self.gradesRepo.getAllForStudent("1"), [grade1, grade2])

    def testRemoveDisciplineGradesByID(self):
        grade1 = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(5, "1", "1")
        grade3 = domain.grade.Grade(5, "1", "2")
        self.gradesRepo.addGrade(grade1)
        self.gradesRepo.addGrade(grade2)
        self.gradesRepo.addGrade(grade3)
        self.gradesRepo.removeDisciplineGradesByID("1")
        self.assertEqual(self.gradesRepo.getAllGrades(), [grade3])
        self.assertRaises(validation.errors.NonExistentIDError, self.gradesRepo.removeDisciplineGradesByID, "300")

    def testGetDisciplineGrades(self):
        grade1 = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(10, "2", "1")
        grade3 = domain.grade.Grade(3, "1", "1")
        grade4 = domain.grade.Grade(5, "1", "2")
        self.gradesRepo.addGrade(grade1)
        self.gradesRepo.addGrade(grade2)
        self.gradesRepo.addGrade(grade3)
        self.gradesRepo.addGrade(grade4)

        self.assertEqual(self.gradesRepo.getDisciplineGrades("1", "1"), [grade1, grade3])


class TestCaseCatalogueFile(unittest.TestCase):

    def testSelectOptionalsByID(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt", "disciplineTest.txt", "optionalsTest.txt")

        student = domain.student.Student("1", "Raul", "Pele")
        discipline1 = domain.discipline.Discipline("2", "Asc", "A", "V", "nu")
        discipline2 = domain.discipline.Discipline("1", "Lc", "A", "P", "da")
        self.catalogueFileRepo.addStudent(student)
        self.catalogueFileRepo.addDiscipline(discipline1)
        self.catalogueFileRepo.addDiscipline(discipline2)

        self.catalogueFileRepo.selectOptionalsByID("1", "1")
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt", "disciplineTest.txt", "optionalsTest.txt")
        optional = student.getOptionals()[0]
        self.assertEqual(optional.getID(), discipline2.getID())
        self.assertEqual(optional.getName(), discipline2.getName())
        self.assertEqual(optional.getTeacherFirst(), discipline2.getTeacherFirst())
        self.assertEqual(optional.getTeacherLast(), discipline2.getTeacherLast())
        self.assertEqual(optional.getIsOptional(), discipline2.getIsOptional())

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

    def testAddStudent(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt", "disciplineTest.txt", "optionalsTest.txt")
        student = domain.student.Student("1", "Raul", "Pele")
        self.catalogueFileRepo.addStudent(student)
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt", "disciplineTest.txt", "optionalsTest.txt")

        result = self.catalogueFileRepo.getStudents()[0]
        self.assertEqual(student.getID(), result.getID())
        self.assertEqual(student.getName(), result.getName())

    def testAddDiscipline(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt", "disciplineTest.txt", "optionalsTest.txt")
        discipline1 = domain.discipline.Discipline("2", "Asc", "A", "V", "nu")
        self.catalogueFileRepo.addDiscipline(discipline1)
        discipline2 = domain.discipline.Discipline("1", "Lc", "A", "P", "da")
        self.catalogueFileRepo.addDiscipline(discipline2)

        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt", "disciplineTest.txt", "optionalsTest.txt")

        self.assertTrue(self.equalDisciplines(self.catalogueFileRepo.getDisciplines(), [discipline1, discipline2]))

    def testRemoveStudentByID(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt", "disciplineTest.txt", "optionalsTest.txt")
        student = domain.student.Student("1", "Raul", "Pele")
        student2 = domain.student.Student("2", "a", "b")
        self.catalogueFileRepo.addStudent(student)
        self.catalogueFileRepo.addStudent(student2)

        self.catalogueFileRepo.removeStudentByID("1")
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt", "disciplineTest.txt", "optionalsTest.txt")
        self.assertTrue(self.equal(self.catalogueFileRepo.getStudents(), [student2]))

    def testRemoveStudentByName(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt", "disciplineTest.txt", "optionalsTest.txt")
        student = domain.student.Student("1", "Raul", "Pele")
        student2 = domain.student.Student("2", "Raul", "Pele")
        self.catalogueFileRepo.addStudent(student)
        self.catalogueFileRepo.addStudent(student2)
        self.catalogueFileRepo.removeStudentByName("Raul Pele")
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt", "disciplineTest.txt", "optionalsTest.txt")
        self.assertEqual(len(self.catalogueFileRepo.getStudents()), 0)

    def testRemoveDisciplineByID(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")
        discipline1 = domain.discipline.Discipline("2", "Asc", "A", "V", "nu")
        self.catalogueFileRepo.addDiscipline(discipline1)
        discipline2 = domain.discipline.Discipline("1", "Lc", "A", "P", "da")
        self.catalogueFileRepo.addDiscipline(discipline2)

        self.catalogueFileRepo.removeDisciplineByID("1")
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")
        self.assertTrue(self.equalDisciplines(self.catalogueFileRepo.getDisciplines(), [discipline1]))

    def testRemoveDisciplineByName(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")
        discipline1 = domain.discipline.Discipline("2", "Asc", "A", "V", "nu")
        self.catalogueFileRepo.addDiscipline(discipline1)
        discipline2 = domain.discipline.Discipline("1", "Asc", "A", "P", "da")
        self.catalogueFileRepo.addDiscipline(discipline2)
        self.catalogueFileRepo.removeDisciplineByName("Asc")
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")
        self.assertEqual(len(self.catalogueFileRepo.getDisciplines()), 0)

    def testRemoveOptionalsByID(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")
        discipline1 = domain.discipline.Discipline("2", "Asc", "A", "V", "nu")
        self.catalogueFileRepo.addDiscipline(discipline1)
        discipline2 = domain.discipline.Discipline("1", "Asc", "A", "P", "da")
        self.catalogueFileRepo.addDiscipline(discipline2)
        student = domain.student.Student("1", "Raul", "Pele")
        self.catalogueFileRepo.addStudent(student)
        self.catalogueFileRepo.selectOptionalsByID("1", "1")
        self.catalogueFileRepo.removeOptionalsByID("1", "1")
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")

        self.assertEqual(len(student.getOptionals()), 0)

    def testModifyDiscID(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")
        discipline1 = domain.discipline.Discipline("2", "Asc", "A", "V", "nu")
        self.catalogueFileRepo.addDiscipline(discipline1)
        discipline2 = domain.discipline.Discipline("1", "Asc", "A", "P", "da")
        self.catalogueFileRepo.addDiscipline(discipline2)

        self.catalogueFileRepo.modifyDiscID(discipline2.getID(), "100")
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")
        result = self.catalogueFileRepo.findDisciplineByID("100")
        self.assertTrue(self.equalDisciplines([result], [discipline2]))

    def testModifyDiscName(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")
        discipline1 = domain.discipline.Discipline("2", "Asc", "A", "V", "nu")
        self.catalogueFileRepo.addDiscipline(discipline1)

        self.catalogueFileRepo.modifyDiscName(discipline1.getID(), "Arhitectura Sistemelor De Calcul")
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")
        self.assertTrue(self.equalDisciplines(self.catalogueFileRepo.findDisciplineByName("Arhitectura Sistemelor De Calcul"), [discipline1]))

    def testModifyDiscOptional(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")
        discipline1 = domain.discipline.Discipline("2", "Asc", "A", "V", "nu")
        self.catalogueFileRepo.addDiscipline(discipline1)
        self.catalogueFileRepo.modifyDiscOptional(discipline1.getID(), True)
        self.assertEqual(self.catalogueFileRepo.findDisciplineByID("2").getIsOptional(), True)

    def testModifyDiscTeacher(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")
        discipline1 = domain.discipline.Discipline("2", "Asc", "A", "V", "nu")
        self.catalogueFileRepo.addDiscipline(discipline1)
        self.catalogueFileRepo.modifyDiscTeacher(discipline1.getID(), "Alexandru", "Vancea")

        self.assertEqual(self.catalogueFileRepo.findDisciplineByID("2").getTeacherFirst(), "Alexandru")
        self.assertEqual(self.catalogueFileRepo.findDisciplineByID("2").getTeacherLast(), "Vancea")
        self.assertRaises(validation.errors.NonExistentIDError, self.catalogueFileRepo.modifyDiscTeacher, "1000000","a", "v" )

    def testModifyStudentID(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")
        student = domain.student.Student("1", "Raul", "Pele")
        self.catalogueFileRepo.addStudent(student)
        self.catalogueFileRepo.modifyStudentID(student.getID(), "1000")
        student.setID("1000")

        self.assertTrue(self.equal([self.catalogueFileRepo.findStudentByID("1000")], [student]))

    def testModifyStudentName(self):
        self.catalogueFileRepo = data.repositories.catalogueFileRepo.CatalogueFileRepository("studentsTest.txt",
                                                                                             "disciplineTest.txt",
                                                                                             "optionalsTest.txt")
        student = domain.student.Student("1", "Raul", "Pele")
        self.catalogueFileRepo.addStudent(student)
        self.catalogueFileRepo.modifyStudentName(student.getID(), "A", "A")
        self.assertEqual(self.catalogueFileRepo.findStudentByID("1").getName(), "A A")
        self.assertRaises(validation.errors.NonExistentIDError, self.catalogueFileRepo.modifyStudentName, "1923123", "a", "b")


    def tearDown(self):
        if os.path.exists("studentsTest.txt"):
            os.remove("studentsTest.txt")

        if os.path.exists("disciplineTest.txt"):
            os.remove("disciplineTest.txt")

        if os.path.exists("optionalsTest.txt"):
            os.remove("optionalsTest.txt")


class TestCaseGradesFileRepo(unittest.TestCase):

    def testAddGrade(self):
        self.gradesFileRepo = data.repositories.GradesFileRepo.GradesFileRepository("gradesTest.txt")
        grade = domain.grade.Grade(10, "1", "1")
        self.gradesFileRepo.addGrade(grade)
        self.gradesFileRepo = data.repositories.GradesFileRepo.GradesFileRepository("gradesTest.txt")
        self.assertEqual(self.gradesFileRepo.getAllGrades(), [grade])

    def testRemoveGrade(self):
        self.gradesFileRepo = data.repositories.GradesFileRepo.GradesFileRepository("gradesTest.txt")
        grade = domain.grade.Grade(10, "1", "1")
        self.gradesFileRepo.addGrade(grade)
        self.gradesFileRepo.removeGrade(grade)
        self.gradesFileRepo = data.repositories.GradesFileRepo.GradesFileRepository("gradesTest.txt")
        self.assertEqual(len(self.gradesFileRepo.getAllGrades()), 0)

    def testRemoveDisciplineGradesByID(self):
        self.gradesFileRepo = data.repositories.GradesFileRepo.GradesFileRepository("gradesTest.txt")
        grade = domain.grade.Grade(10, "1", "1")
        grade2 = domain.grade.Grade(5, "1", "1")
        grade3 = domain.grade.Grade(3, "1", "2")
        self.gradesFileRepo.addGrade(grade)
        self.gradesFileRepo.addGrade(grade2)
        self.gradesFileRepo.addGrade(grade3)
        self.gradesFileRepo.removeDisciplineGradesByID("1")
        self.gradesFileRepo = data.repositories.GradesFileRepo.GradesFileRepository("gradesTest.txt")
        self.assertEqual(self.gradesFileRepo.getAllGrades(), [grade3])

    def tearDown(self):
        if os.path.exists("gradesTest.txt"):
            os.remove("gradesTest.txt")

if __name__ == "__main__":
    unittest.main()
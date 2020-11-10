import data.repositories.catalogue
import domain.student
import validation.errors

class Tests:

    def equal(self, list1, list2):
        if len(list1) != len(list2):
            return False
        for i in range(0, len(list1)):
            if list1[i] != list2[i]:
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

        student = domain.student.Student("123", "Raul", "Pele")
        try:
            catalogue.addStudent(student)
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

    def runTests(self):
        self.testAddStudent()

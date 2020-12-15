
from validation.errors import StudentAlreadyExistsError, DisciplineAlreadyExistsError, NonExistentIDError
from validation.errors import NonExistentStudentError, NonExistentDisciplineError

class Catalogue():

    def __init__(self):
        self.__students = []
        self.__disciplines = []

    def __enrollStudent(self, newStudent):
        """
        Ii atribuie studentului newStudent disciplinele obligatorii din catalog
        :param newStudent: obiect Student
        """
        for discipline in self.__disciplines:
            if  discipline.getIsOptional() == False:
                newStudent.addDiscipline(discipline)

    def addStudent(self, newStudent):
        """
        Adauga studentul newStudent pe pozitia corespunzatoare in lista de studenti
        in ordine alfabetica
        raise StudentAlreadyExistsError daca student se afla deja in lista
        :param newStudent: obiect Student
        """
        oldSize = len(self.__students)
        if oldSize == 0:
            self.__students.append(newStudent)
            self.__enrollStudent(newStudent)
            return

        if newStudent in self.__students:
            raise StudentAlreadyExistsError("Studentul se afla deja in lista!\n")

        for i in range(0, oldSize):
            currentStudent = self.__students[i]
            if newStudent.getLastName() < currentStudent.getLastName() or\
                    (newStudent.getLastName() == currentStudent.getLastName() and
                    newStudent.getFirstName() < currentStudent.getFirstName()):
                self.__students.insert(i, newStudent)
                break

        if oldSize == len(self.__students):
            self.__students.append(newStudent)

        self.__enrollStudent(newStudent)

    def addDisciplineToStudents(self, newDiscipline):
        """
        Adauga disciplina obligatorie newDiscipline in lista de discipline a studentilor din catalog
        :param newDiscipline: disciplina Discipline()
        """
        for student in self.__students:
            student.addDiscipline(newDiscipline)

    def addDiscipline(self, newDiscipline):
        """
        Adauga disciplina newDiscipline pe pozitia corespunzatoare pentru a respecta
        ordonarea alfabetica a listei de discipline
        raise DisciplineAlreadyExists - daca disciplina exista deja in lista
        :param newDiscipline: obiect Discipline()
        """
        oldSize = len(self.__disciplines)
        if oldSize == 0:
            self.__disciplines.append(newDiscipline)
            if newDiscipline.getIsOptional() == False:
                self.addDisciplineToStudents(newDiscipline)
            return

        if newDiscipline in self.__disciplines:
            raise DisciplineAlreadyExistsError("Disciplina exista deja in facultate!\n")

        for i in range(0, oldSize):
            currentDiscipline = self.__disciplines[i]
            if currentDiscipline.getName() > newDiscipline.getName():
                self.__disciplines.insert(i, newDiscipline)
                break

        if oldSize == len(self.__disciplines):
            self.__disciplines.append(newDiscipline)

        if newDiscipline.getIsOptional() == False:
            self.addDisciplineToStudents(newDiscipline)


    def removeStudentByID(self, ID):
        """
        Sterge studentul identificat cu ID din lista
        raise NonExistentStudentError - daca nu exista student cu id-ul ID in lista
        :param ID: string - id-ul studentului
        """
        """
        Analiza complexitatii functiei:
        students = list of students (self.__students)

        BC(removeStudentByID) = min E(I) -> E(I)- numar de operatii efectuate, I <- students
        -> acesta este cazul in care stundetul care va fi sters se afla pe prima pozitie in lista (best case scenario)
        BC(removeStudentByID) = 1 <=> T(n) = 1 ∈ 𝛩(1) 

        WC(removeStudentByID) = max E(students)
        -> cazul in care studentul nu se afla in lista sau se afla pe ultima pozitie (Worst Case Scenario)
        WC(removeStudentByID) = n <=> T(n) = n ∈ 𝛩(n)
        
        AC(removeStudentByID) = Sum(P(I)*E(I)) -> P = probabilitatea de avea I ca si date de intrare, I <- students
        T(n) = (1+2+3+...+n)/n = n*(n+1)/2*n = (n+1)/2
        T(n) = (n+1)/2 ∈ 𝛩(n) 
        
        Overall complexity: O(n)
        
        """

        for i in range(0, len(self.__students)):
            student = self.__students[i]
            if student.getID() == ID:
                del self.__students[i]
                return
        raise NonExistentStudentError("Studentul cu ID-ul dat nu se afla in lista!\n")

    def removeStudentByName(self, name):
        """
        Sterge din lista de studenti studentul (sau studentii) cu numele name
        name - string
        raise NonExistentStudentError - daca nu exista studentul in lista
        """
        studentsDeleted = False
        i=0
        while i < len(self.__students):
            student = self.__students[i]
            if student.getName().lower() == name.lower():
                del self.__students[i]
                studentsDeleted = True
                continue
            i+=1

        if not studentsDeleted:
            raise NonExistentStudentError("Studentul cu numele dat nu se afla in lista!\n")

    def removeDisciplineForStudents(self, discipline):
        """
        Sterge disciplina discipline din lista de discipline a studentilor
        :param discipline: obiect de tip Discipline()
        """
        for student in self.__students:
            student.removeDiscipline(discipline)

    def removeDisciplineByID(self, ID):
        """
        Sterge disciplina identificata cu ID din lista de discipline a catalogului
        :param ID: id-ul disciplinei - string
        raise NonExistentIDError - in cazul in care disciplina cu id-ul ID nu se afla in lista
        """
        for i in range(0, len(self.__disciplines)):
            discipline = self.__disciplines[i]
            if discipline.getID() == ID:
                self.removeDisciplineForStudents(discipline)
                del self.__disciplines[i]
                return
        raise NonExistentIDError("Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n")

    def removeDisciplineByName(self, name):
        """
        Sterge disciplina cu numele name din lista de discipline
        raise NonExistentDisciplineError: daca disciplina nu exista
        :param name: nume - string
        """
        i = 0
        disciplinesDeleted = False
        while i < len(self.__disciplines):
            discipline = self.__disciplines[i]
            if discipline.getName().lower() == name.lower():
                self.removeDisciplineForStudents(discipline)
                del self.__disciplines[i]
                disciplinesDeleted = True
                continue
            i += 1

        if not disciplinesDeleted:
            raise NonExistentDisciplineError("Disciplina cu numele dat nu se afla in lista!\n")


    def findStudentByID(self, ID, i=0):
        """
        Returneaza studentul cu id-ul ID din lista
        raise NonExistentIDError - daca studentul nu exista in lista
        :param ID: id-ul studentului - string
        :param i: contor pentru recursivitate
        """

        # for student in self.__students:
        #     if student.getID() == ID:
        #         return student
        # raise NonExistentIDError("Studentul cu ID-ul dat nu se afla in lista studentilor!\n")

        if i >= len(self.__students):
            raise NonExistentIDError("Studentul cu ID-ul dat nu se afla in lista studentilor!\n")
        else:
            if self.__students[i].getID() == ID:
                return self.__students[i]
            else:
                return self.findStudentByID(ID, i+1)



    def findStudentByName(self, name):
        """
        Returneaza studentii cu numele name din lista
        raise NonExistentStudentError - daca nu exista studenti cu numele name
        :param name: nume - string
        :return students: lista de studenti
        """
        students=[]
        for student in self.__students:
            if student.getName().lower() == name.lower():
                students.append(student)

        if len(students) == 0:
            raise NonExistentStudentError("Studentul cu numele dat nu se afla in lista!\n")
        return students

    def findDisciplineByID(self, ID, i=0):
        """
        Returneaza studentul cu id-ul ID din lista
        raise NonExistentIDError - daca disciplina nu exista in lista
        :param ID:  id-ul disciplinei - string
        """
        # for discipline in self.__disciplines:
        #     if discipline.getID() == ID:
        #         return discipline
        # raise NonExistentIDError("Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n")

        if i>=len(self.__disciplines):
            raise NonExistentIDError("Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n")
        else:
            if self.__disciplines[i].getID() == ID:
                return self.__disciplines[i]
            else:
                return self.findDisciplineByID(ID, i+1)

    def findDisciplineByName(self, name):
        """
        Returneaza toate disciplinele cu numele name din lista de discipline
        :param name: numele disciplinelor care se cauta - string
        :return disciplines: lista de discipline corespunzatoare
        raise NonExistentDisciplineError - daca nu exista nicio disciplina cu numele name
        """
        disciplines = []
        for d in self.__disciplines:
            if d.getName().lower() == name.lower():
                disciplines.append(d)
        if len(disciplines) == 0:
            raise NonExistentDisciplineError("Disciplina cu numele dat nu se afla in lista!\n")
        return disciplines

    def selectOptionalsByID(self, IDStudent, IDDiscipline):
        """
        Adauga disciplina optionala IDDiscipline studentului IDStudent
        :param IDStudent:
        :param IDDiscipline:
        raise NonExistentIDError daca studentul sau disciplina nu se regasesc in catalog
        :return:
        """
        try:
            student = self.findStudentByID(IDStudent)
            discipline = self.findDisciplineByID(IDDiscipline)
            if not discipline.getIsOptional():
                raise NonExistentIDError("Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n")
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))
        else:
            student.addDiscipline(discipline)

    def removeOptionalsByID(self, IDStudent, IDDiscipline):
        """
        Sterge disciplina optionala IDDiscipline din lista de discipline a studentului IDSTudent
        :param IDStudent: id-ul studentului -string
        :param IDDiscipline: id-ul disciplinei -string
        raise NonExistentIDError daca studentul sau disciplina nu se regasesc in catalog
        """
        try:
            student = self.findStudentByID(IDStudent)
            discipline = self.findDisciplineByID(IDDiscipline)
            if not discipline.getIsOptional():
                raise NonExistentIDError("Disciplina cu ID-ul dat nu se afla in lista disciplinelor!\n")
        except NonExistentIDError as err:
            raise NonExistentIDError(str(err))
        else:
            student.removeDiscipline(discipline)

    def modifyStudentName(self, student, newFirstName, newLastName):
        """
        Modifica numele studentului student in newFirstName si newLastName
        :param student: obiect Student()
        :param newFirstName: noul prenume - string
        :param newLastName: noul nume - string
        """
        for st in self.__students:
            if st == student:
                st.setName(newFirstName, newLastName)

    def modifyStudentID(self, student, newID):
        """
        Modifica id-ul studentului student in newID
        :param student: obiect Student()
        :param newID: noul id - string
        """
        for st in self.__students:
            if st == student:
                st.setID(newID)
                return

    def modifyDiscID(self, discipline, newID):
        """
        Modifica id-ul disciplinei discipline in newID
        :param discipline: Discipline()
        :param newID: id-ul nou - string
        """
        discipline.setID(newID)

    def modifyDiscName(self, discipline, newName):
        """
        Modifica numele disciplinei discipline in newName
        :param discipline: obiect Discipline()
        :param newName: noul nume - string
        """
        discipline.setName(newName)

    def modifyDiscTeacher(self, discipline, newFirstName, newLastName):
        """
        Modifica numele profesorului disciplinei discipline in newFirstName + newLastName
        :param discipline: disciplina Discipline()
        :param newFirstName: noul prenume - string
        :param newLastName: noul nume - string
        """
        discipline.setTeacherFirst(newFirstName)
        discipline.setTeacherLast(newLastName)

    def modifyDiscOptional(self, discipline, isOptional):
        """
        Modifica caracterul disciplinei discipline
        :param discipline: Discipline()
        :param isOptional: caracterul disciplinei - bool
        """
        oldOptional = discipline.getIsOptional()
        discipline.setOptional(isOptional)

        if oldOptional == False and isOptional == True:
            #was not optional before but now it is
            self.removeDisciplineForStudents(discipline)
        elif oldOptional == True and isOptional == False:
            #was optional before but now it's not
            self.addDisciplineToStudents(discipline)

    def getStudents(self):
        return self.__students

    def getDisciplines(self):
        return self.__disciplines

    def getOptionals(self):
        optionals = []
        for discipline in self.getDisciplines():
            if discipline.getIsOptional():
                optionals.append(discipline)
        return optionals


    def clearStudentsList(self):
        self.__students.clear()

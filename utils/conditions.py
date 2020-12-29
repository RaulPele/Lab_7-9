
def studentDTONameGrade(student1, student2):
    if student1.getAverage() < student2.getAverage() or (student1.getAverage() == student2.getAverage() and student1.getStudent().getName() < student2.getStudent().getName()):
        return True
    return False





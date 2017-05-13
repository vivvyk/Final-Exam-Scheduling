import random
import itertools
import copy

'''
def sectioncondense(course):
    j = 0
    for i in course:
        if i.isdigit():
            deptlen = j
            break
        j += 1
    course = course[:deptlen+3]
    return course
'''

def precomp(studentcourses,exams):
    S = []
    '''
    for i in range(len(exams)):
        exams[i] = sectioncondense(exams[i])
    for i in range(len(studentcourses)):
        for j in range(len(studentcourses[i])):
            studentcourses[i][j] = sectioncondense(studentcourses[i][j])
    '''
    for student in studentcourses:
        newstudent = []
        examcounter = 0
        for course in student:
            if course in exams:
                examcounter += 1
                newstudent.append(course)
        if examcounter > 1:
            S.append(newstudent)
    return S

def flatten(l):
    newl =[]
    for sub in l:
        for x in sub:
            newl.append(x)
    return newl

def evaluate_variable(variables,courses,block_number):
    blocked = []
    for i in range(block_number):
        blocked.append([])
    for variable in variables:
        blocked[variable[1]-1].append(variable[0])

    conflictArray = []
    for block in blocked:
        conflictions = list(itertools.combinations(block,2))
        for conflict in conflictions:
            for student in courses:
                if conflict[0] in student and conflict[1] in student:
                    conflictArray.append(conflict)

    if len(conflictArray) == 0:
        return None

    conflict_d = {}
    for conflict in conflictArray:
        if not conflict[0] in conflict_d:
            conflict_d[conflict[0]] = 1
        else:
            conflict_d[conflict[0]] += 1

        if not conflict[1] in conflict_d:
            conflict_d[conflict[1]] = 1
        else:
            conflict_d[conflict[1]] += 1

    var_max_conflicts = max(conflict_d, key = conflict_d.get)
    total_conflicts = sum(conflict_d.values())

    return (var_max_conflicts,total_conflicts)

def reset_A(variables,courses,block_number,variable):
    valArray = []
    newA = dict(variables)

    for value in range(1,block_number):
        if value == newA[variable]:
            continue

        newA[variable] = value
        A = [(k,v) for k,v in newA.iteritems()]
        evalN = evaluate_variable(A, courses, block_number)
        if evalN is None:
            return (0,A)
        valArray.append((value,evalN[1]))


    newval = min(valArray,key=lambda item:item[1])[0]
    newA[variable] = newval
    A = [(k,v) for k,v in newA.iteritems()]
    return A



def local_search(exams, courses, block_number):
    attempt_Counter = 0
    while attempt_Counter < 100:
        A = [(exam,random.randint(1,block_number)) for exam in exams]
        tabu_list = []
        for i in range(45):
            eval_var = evaluate_variable(A,courses,block_number)
            A = reset_A(A,courses,block_number,eval_var[0])
            if A in tabu_list:
                break
            tabu_list.append(A)
            if len(A) == 2:
                return A[1]
        attempt_Counter += 1
    return None




if __name__ == "__main__":
    coursereader = open("StudentCourses17.txt", "r")
    examreader = open("exams.txt", "r")

    courses = coursereader.readlines()
    courses = [i.strip("\n").replace(" ","").split(",") for i in courses]

    exams = examreader.readlines()
    exams = flatten([i.strip("\n").replace(" ","").split(",") for i in exams])

    trunc_courses = precomp(courses,exams)

    exam_schedule =  local_search(exams,trunc_courses,9)

    blocked = []
    for i in range(9):
        blocked.append([])

    for exam in exam_schedule:
        blocked[exam[1]-1].append(exam[0])

    for index,block in enumerate(blocked):
        print index+1
        for item in block:
            print item
        print "\n"

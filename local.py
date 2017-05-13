import random
import itertools
import copy
import time
import sys

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


def sectioncondense2(course):
    if course[-1] in "ABCDEF":
        return course[:-1]
    return course
'''


def precomp(studentcourses,exams):
    S = []
    # print studentcourses
    for student in studentcourses:
        newstudent = []
        examcounter = 0
        for course in student:
            if course in exams:
                examcounter += 1
                newstudent.append(course)
        if examcounter > 1:
            exams = [course.rstrip('ABCDEFGHIJKLMNOP') for course in exams]
            newstudent = [course.rstrip('ABCDEFGHIJKLMNOP') for course in newstudent]
            exams = [exam.rstrip('ABCDEFGHIJKLMNOP') for exam in exams]
            exams = list(set(exams))
            S.append(newstudent)
    return exams, S

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
        # print "Resetting"
        A = [(exam,random.randint(1,block_number)) for exam in exams]
        tabu_list = []
        for i in range(100):
            eval_var = evaluate_variable(A,courses,block_number)
            # print eval_var
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

    exams, trunc_courses = precomp(courses,exams)

    start = time.time()
    solution = None
    minimax = sys.maxint
    for i in range(10):
        exam_schedule = local_search(exams,trunc_courses,9)
        if exam_schedule is None:
            print "No solution found"
            continue
        print "Solution found"
        blocked = []
        for i in range(9):
            blocked.append([])

        for exam in exam_schedule:
            blocked[exam[1]-1].append(exam[0])
        
        maximum = -1

        for block in blocked:
            if len(block) > maximum:
                maximum = len(block)

        if maximum < minimax:
            print "Updating best solution..."
            solution = blocked
            minimax = maximum

    end = time.time()

    print exam_schedule

    print evaluate_variable(exam_schedule, trunc_courses, 9)

    for index,block in enumerate(solution):
        print index+1
        for item in block:
            print item
        print "\n"

    print "Runtime: " + str(end - start) + " seconds"

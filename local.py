import random
import itertools
import copy
import time
import sys


def precomp(studentcourses,exams):
    '''
    Precomputation step: gets rid of students with fewer than 2 exams,
    gets rid of courses that don't have an exam, and disregards/labs and other sections.

    @param studentcourses: the list of courses being taken by every student.
    @param exams: the list of exams.
    @return: a combined exam list, cut/combined student course list.
    '''
    S = []
    for student in studentcourses:
        newstudent = []
        examcounter = 0
        for course in student:
            if course in exams:
                examcounter += 1
                newstudent.append(course) #Cuts courses that do not have an exam.

        if examcounter > 1: #If the student does not have fewer than 2 exams, strips sections and labs, and appends the course for processing.
            newstudent = [course.rstrip('ABCDEFGHIJKLMNOP') for course in newstudent]
            newstudent = list(set(newstudent))
            S.append(newstudent)

    #Strips exams
    exams = [exam.rstrip('ABCDEFGHIJKLMNOP') for exam in exams]
    exams = list(set(exams))

    return exams, S

def flatten(l):
    '''
    Flattens array; turns 2D array into 1D

    @param l: 2D array
    @return: 1D array
    '''
    newl =[]
    for sub in l:
        for x in sub:
            newl.append(x)
    return newl

def evaluate_variable(variables,courses,block_number):
    '''
    Picks the next variable to change. This variable must participate in the largest number of conflicts.

    @param variables:
    '''
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

    # Best solution so far
    solution = None

    # Smallest maximum amount of courses in a time slot
    minimax = sys.maxint

    # Refinement level, call local search repeatedly
    for i in range(int(sys.argv[1])):
        exam_schedule = local_search(exams,trunc_courses,9)
        if exam_schedule is None:
            print "No solution found"
            continue
        print "Solution found"

        # Convert results so it can be indexed by block number
        blocked = []
        for i in range(9):
            blocked.append([])

        for exam in exam_schedule:
            blocked[exam[1]-1].append(exam[0])


        # Find the maximum
        maximum = -1

        for block in blocked:
            if len(block) > maximum:
                maximum = len(block)

        # Find the minimum
        if maximum < minimax:
            print "Updating best solution..."
            solution = blocked
            minimax = maximum

    end = time.time()

    # Print out the schedule
    for index,block in enumerate(solution):
        print index+1
        for item in block:
            print item
        print "\n"

    print "Runtime: " + str(end - start) + " seconds"

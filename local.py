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

    @param variables: variables; exams with random assigned values.
    @param courses: courses for every student.
    @param block_number: number of exam blocks.
    @return: the varible that participates in the most conflicts, the total number of conflicts for the current exam configuration.
    '''
    #Organizes exams into blocks.
    blocked = []
    for i in range(block_number):
        blocked.append([])
    for variable in variables:
        blocked[variable[1]-1].append(variable[0])

    #Finds all conflicting exams.
    conflictArray = []
    for block in blocked:
        conflictions = list(itertools.combinations(block,2)) #All possible combinations of 2 for the same block
        for conflict in conflictions:
            for student in courses:
                if conflict[0] in student and conflict[1] in student: #If both exams are shared by a student, then there is a conflict. #This violates our constraint.
                    conflictArray.append(conflict)

    if len(conflictArray) == 0: #Current exam configuration is a solution.
        return None

    conflict_d = {} #This dictionary assigns a conflict score for each variable (number of times it appears in a conflicting tuple)
    for conflict in conflictArray:
        if not conflict[0] in conflict_d:
            conflict_d[conflict[0]] = 1
        else:
            conflict_d[conflict[0]] += 1 #Increments for each participation of first exam

        if not conflict[1] in conflict_d:
            conflict_d[conflict[1]] = 1
        else:
            conflict_d[conflict[1]] += 1 #Increments for each participation of second exam.

    var_max_conflicts = max(conflict_d, key = conflict_d.get) #Exam in most conflictions
    total_conflicts = sum(conflict_d.values()) #Total conflictions

    return (var_max_conflicts,total_conflicts)

def pick_value(variables,courses,block_number,variable):
    '''
    Given the variable with the most conflictions, we pick the value that minimizes total conflictions.

    @param variables: variables; exams with random assigned values.
    @param courses: courses for every student.
    @param block_number: number of exam blocks.
    @param variable: the variable that participates in the most conflicts.
    @return: variable array with a new value for the chosen variable.
    '''
    valArray = []
    newA = dict(variables)

    #Try every value except current value
    for value in range(1,block_number):
        if value == newA[variable]: #Ignores current variable
            continue

        newA[variable] = value #Assigns new value
        A = [(k,v) for k,v in newA.iteritems()] #Turns back into list

        evalN = evaluate_variable(A, courses, block_number) #Gets total number of courses
        if evalN is None: #Solution found.
            return (0,A)
        valArray.append((value,evalN[1])) #Assigns conflict number to value.


    newval = min(valArray,key=lambda item:item[1])[0] #Finds value with min conflict number
    newA[variable] = newval #Assigns to variable list
    A = [(k,v) for k,v in newA.iteritems()]
    return A



def local_search(exams, courses, block_number):
    '''
    Runs local search algorithm.

    @@param exams: exams with random assigned values.
    @param courses: courses for every student.
    @param block_number: number of exam blocks.
    @return:
    '''
    attempt_Counter = 0 #Threshold 1: The number of times we will reset before giving up.
    while attempt_Counter < 100:
        A = [(exam,random.randint(1,block_number)) for exam in exams] #Assigns random values
        tabu_list = [] #Tabu list
        for i in range(100): #Threshold 2: how long traverse the graph. Will disctontinue if a cycle is found.

            #Picks variable and value.
            eval_var = evaluate_variable(A,courses,block_number)
            A = pick_value(A,courses,block_number,eval_var[0])

            if A in tabu_list: #Cycle
                break
            tabu_list.append(A)

            if len(A) == 2: #Solution found
                return A[1]

        attempt_Counter += 1
    return None




if __name__ == "__main__":
    coursereader = open("StudentCourses17.txt", "r")
    examreader = open("exams.txt", "r")

    courses = coursereader.readlines()
    courses = [i.strip("\n").replace(" ","").split(",") for i in courses] #Turns courses into array of courses for each student.

    exams = examreader.readlines()
    exams = flatten([i.strip("\n").replace(" ","").split(",") for i in exams]) #Creates array of exams.

    exams, trunc_courses = precomp(courses,exams) #Precomputation

    start = time.time()

    solution = None
    minimax = sys.maxint
    for i in range(int(sys.argv[1])):
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

    for index,block in enumerate(solution):
        print index+1
        for item in block:
            print item
        print "\n"

    print "Runtime: " + str(end - start) + " seconds"
